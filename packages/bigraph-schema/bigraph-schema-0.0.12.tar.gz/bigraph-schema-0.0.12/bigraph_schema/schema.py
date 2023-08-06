import copy
import pprint
import pytest

from bigraph_schema.parse import parse_expression
from bigraph_schema.registry import Registry, TypeRegistry, RegistryRegistry, type_schema_keys, optional_schema_keys, deep_merge, get_path, establish_path, set_path, remove_path, non_schema_keys
from bigraph_schema.units import units, render_units_type, parse_dimensionality


class SchemaTypes():
    def __init__(self):
        self.apply_registry = Registry()
        self.serialize_registry = Registry()
        self.deserialize_registry = Registry()
        self.divide_registry = Registry()
        self.type_registry = TypeRegistry()

        self.registry_registry = RegistryRegistry()
        self.registry_registry.register('_type', self.type_registry)
        self.registry_registry.register('_apply', self.apply_registry)
        self.registry_registry.register('_divide', self.divide_registry)
        self.registry_registry.register('_serialize', self.serialize_registry)
        self.registry_registry.register('_deserialize', self.deserialize_registry)
        
        register_base_types(self)


    def access(self, type_key):
        return self.type_registry.access(type_key)


    def validate_schema(self, schema, enforce_connections=False):
        # add ports and wires
        # validate ports are wired to a matching type,
        #   either the same type or a subtype (more specific type)
        # declared ports are equivalent to the presence of a process
        #   where the ports need to be looked up

        report = {}

        if schema is None:
            report = 'schema cannot be None'

        elif isinstance(schema, str):
            typ = self.access(schema)
            if typ is None:
                report = f'type: {schema} is not in the registry'

        elif isinstance(schema, dict):
            report = {}

            schema_keys = set([])
            branches = set([])

            for key, value in schema.items():
                if key == '_type':
                    typ = self.access(value)
                    if typ is None:
                        report[key] = f'type: {value} is not in the registry'
                elif key in type_schema_keys:
                    schema_keys.add(key)
                    registry = self.registry_registry.access(key)
                    if registry is None:
                        # deserialize and serialize back and check it is equal
                        pass
                    else:
                        element = registry.access(value)
                        if element is None:
                            report[key] = f'no entry in the {key} registry for: {value}'
                else:
                    branches.add(key)
                    branch_report = self.validate_schema(value)
                    if len(branch_report) > 0:
                        report[key] = branch_report

        return report


        # # We will need this when building states to check to see if we are
        # # trying to instantiate an abstract type, but we can still register
        # # register abstract types so it is not invalid
        # if len(schema_keys) > 0 and len(branches) == 0:
        #     undeclared = set(type_schema_keys) - schema_keys
        #     if len(undeclared) > 0:
        #         for key in undeclared:
        #             if not key in optional_schema_keys:
        #                 report[key] = f'missing required key: {key} for declaring atomic type'



    # TODO: if its an edge, ensure ports match wires
    def validate_state(self, original_schema, state):
        schema = self.access(original_schema)
        validation = {}

        if '_serialize' in schema:
            if '_deserialize' not in schema:
                validation = {
                    '_deserialize': f'serialize found in type without deserialize: {schema}'
                }
            else:
                serialize = self.serialize_registry.access(
                    schema['_serialize'])
                deserialize = self.deserialize_registry.access(
                    schema['_deserialize'])
                serial = serialize(state)
                pass_through = deserialize(serial)

                if state != pass_through:
                    validation = f'state and pass_through are not the same: {serial}'
        else:
            for key, subschema in schema.items():
                if key not in type_schema_keys:
                    if key not in state:
                        validation[key] = f'key present in schema but not in state: {key}\nschema: {schema}\nstate: {state}\n'
                    else:
                        subvalidation = self.validate_state(
                            subschema,
                            state[key])
                        if not (subvalidation is None or len(subvalidation) == 0):
                            validation[key] = subvalidation

        return validation


    def default(self, schema):
        default = None
        found = self.access(schema)

        if '_default' in found:
            if not '_deserialize' in found:
                raise Exception(
                    f'asking for default for {type_key} but no deserialize in {found}')
            default = self.deserialize(found, found['_default'])
        else:
            default = {}
            for key, subschema in found.items():
                if key not in type_schema_keys:
                    default[key] = self.default(subschema)

        return default
        

    def apply_update(self, schema, state, update):
        if '_apply' in schema:
            apply_function = self.apply_registry.access(schema['_apply'])
            
            state = apply_function(
                state,
                update,
                schema.get('_bindings'),
                self)

        elif isinstance(schema, str) or isinstance(schema, list):
            schema = self.access(schema)
            state = self.apply_update(schema, state, update)

        elif isinstance(update, dict):
            for key, branch in update.items():
                if key not in schema:
                    raise Exception(f'trying to update a key that is not in the schema {key} for state:\n{state}\nwith schema:\n{schema}')
                else:
                    subupdate = self.apply_update(
                        schema[key],
                        state[key],
                        branch)

                    state[key] = subupdate
        else:
            raise Exception(f'trying to apply update\n  {update}\nto state\n  {state}\nwith schema\n{schema}, but the update is not a dict')

        return state


    def apply(self, original_schema, initial, update):
        schema = self.access(original_schema)
        state = copy.deepcopy(initial)
        return self.apply_update(schema, initial, update)


    def serialize(self, schema, state):
        found = self.access(schema)
        if '_serialize' in found:
            serialize_function = self.serialize_registry.access(
                found['_serialize'])

            if serialize_function is None:
                raise Exception(
                    f'serialize function not in the registry: {schema}')
            else:
                return serialize_function(
                    state,
                    found.get('_bindings'),
                    self)
        else:
            tree = {
                key: self.serialize(
                    schema[key],
                    state.get(key))
                for key in non_schema_keys(schema)}

            return repr(tree)
                

    def deserialize(self, schema, encoded):
        found = self.access(schema)

        if '_deserialize' in found:
            deserialize = found['_deserialize']
            if isinstance(deserialize, str):
                deserialize_function = self.deserialize_registry.access(
                    deserialize)
            else:
                deserialize_function = deserialize

            if deserialize_function is None:
                raise Exception(
                    f'deserialize function not in the registry: {deserialize}')

            return deserialize_function(
                encoded,
                found.get('_bindings'),
                self)
        else:
            tree = eval(encoded)
            
            return {
                key: self.deserialize(schema.get(key), branch)
                for key, branch in tree.items()}


    def divide(self, schema, state, ratios=(0.5, 0.5)):
        # TODO: implement
        return state


    def fill_ports(self, schema, wires=None, state=None, top=None, path=()):
        # deal with wires
        if wires is None:
            wires = {}
        if state is None:
            state = {}
        if top is None:
            top = state

        more_wires = state.get('wires', {})
        wires = deep_merge(wires, more_wires)

        for port_key, port_schema in schema.items():
            if port_key in wires:
                subwires = wires[port_key]
                if isinstance(subwires, dict):
                    state[port_key] = fill_ports(
                        port_schema,
                        wires=subwires,
                        state=state.get(port_key),
                        top=top,
                        path=path)
                else:
                    if isinstance(subwires, str):
                        subwires = (subwires,)

                    if len(path) == 0:
                        raise Exception(
                            f'cannot wire {port_key} as we are already at the top level {schema}')

                    peer = get_path(
                        top,
                        path[:-1])

                    destination = establish_path(
                        peer,
                        subwires[:-1],
                        top=top,
                        cursor=path[:-1])

                    destination_key = subwires[-1]

                    if destination_key in destination:
                        pass
                        # validate_state(
                        #     port_schema,
                        #     destination[destination_key])
                    else:
                        destination[destination_key] = self.default(
                            port_schema)
            else:
                # handle unconnected ports
                pass

        return state


    def fill_state(self, schema, state=None, top=None, path=(), type_key=None, context=None):
        # if a port is disconnected, build a store
        # for it under the '_open' key in the current
        # node (?)

        # inform the user that they have disconnected
        # ports somehow

        if schema is None:
            return None
        if state is None:
            state = self.default(schema)
        if top is None:
            top = state

        if '_ports' in schema:
            wires = state.get('wires', {})
            state = self.fill_ports(
                schema['_ports'],
                wires=wires,
                state=state,
                top=top,
                path=path)

        branches = non_schema_keys(schema)
        if len(branches) > 0 and not isinstance(state, dict):
            raise Exception(f'schema has branches\n{schema}\nbut state is a leaf\n{state}')
        else:
            for branch in branches:
                subpath = path + (branch,)
                state[branch] = self.fill_state(
                    schema[branch],
                    state=state.get(branch),
                    top=top,
                    path=subpath)
            
        return state


    def fill(self, original_schema, state=None):
        if state is not None:
            state = copy.deepcopy(state)
        schema = self.access(original_schema)

        return self.fill_state(
            schema,
            state=state)


    def ports_and_wires(self, schema, instance, edge_path):
        found = self.access(schema)

        edge_schema = get_path(found, edge_path)
        ports = edge_schema.get('_ports')
        edge_state = get_path(instance, edge_path)
        wires = edge_state.get('wires')
        
        return ports, wires
    

    def project_state(self, schema, wires, instance, path):
        result = {}
        if isinstance(wires, str):
            wires = [wires]
        if isinstance(wires, list):
            result = get_path(instance, path + wires)
        elif isinstance(wires, dict):
            result = {
                port_key: self.project_state(
                    schema[port_key],
                    wires[port_key],
                    instance,
                    path)
                for port_key in wires}
        else:
            raise Exception(f'trying to project state with these ports:\n{ports}\nbut not sure what these wires are:\n{wires}')

        return result
        

    def project(self, schema, instance, edge_path=()):
        '''
        project the state of the current instance into a form
        the edge expects, based on its ports
        '''

        if schema is None:
            return None
        if instance is None:
            instance = self.default(schema)

        ports, wires = self.ports_and_wires(schema, instance, edge_path=edge_path)

        if ports is None:
            return None
        if wires is None:
            return None

        return self.project_state(
            ports,
            wires,
            instance,
            edge_path[:-1])


    def invert_state(self, ports, wires, path, states):
        result = {}

        if isinstance(wires, str):
            wires = [wires]

        if isinstance(wires, list):
            destination = path + wires
            result = set_path(
                result,
                destination,
                states)

        elif isinstance(wires, dict):
            branches = [
                self.invert_state(
                    ports.get(key),
                    wires[key],
                    path,
                    states.get(key))
                for key in wires.keys()]

            branches = [
                branch
                for branch in branches
                if branch is not None and list(branch)[0][1] is not None]

            result = {}
            for branch in branches:
                deep_merge(result, branch)
        else:
            raise Exception(
                f'inverting state\n  {state}\naccording to ports schema\n  {schema}\nbut wires are not recognized\n  {wires}')

        return result


    def invert(self, schema, instance, edge_path, states):
        '''
        given states from the perspective of an edge (through
          it's ports), produce states aligned to the tree
          the wires point to.
          (inverse of project)
        '''

        if schema is None:
            return None
        if instance is None:
            instance = self.default(schema)

        ports, wires = self.ports_and_wires(schema, instance, edge_path)

        if ports is None:
            return None
        if wires is None:
            return None

        return self.invert_state(
            ports,
            wires,
            edge_path[:-1],
            states)
        

    def link_place(self, place, link):
        pass


    def compose(self, a, b):
        pass


    # maybe vivarium?
    def hydrate(self, schema):
        return {}
    

    def dehydrate(self, schema):
        return {}


    def query(self, schema, instance, redex):
        subschema = {}
        return subschema


    def react(self, schema, instance, redex, reactum):
        return {}


def accumulate(current, update, bindings, types):
    if update is None:
        import ipdb; ipdb.set_trace()
    return current + update

def concatenate(current, update, bindings, types):
    return current + update

# support dividing by ratios?
# ---> divide_float({...}, [0.1, 0.3, 0.6])

def divide_float(value, ratios, bindings, types):
    half = value / 2.0
    return (half, half)

# support function types for registrys?
# def divide_int(value: int, _) -> tuple[int, int]:
def divide_int(value, bindings, types):
    half = value // 2
    other_half = half
    if value % 2 == 1:
        other_half += 1
    return half, other_half


# class DivideRegistry(Registry):
    

# def divide_longest(dimensions: Dimension) -> Tuple[Dimension, Dimension]:
def divide_longest(dimensions, bindings, types):
    # any way to declare the required keys for this function in the registry?
    # find a way to ask a function what type its domain and codomain are

    width = dimensions['width']
    height = dimensions['height']
    
    if width > height:
        a, b = divide_int(width)
        return [{'width': a, 'height': height}, {'width': b, 'height': height}]
    else:
        x, y = divide_int(height)
        return [{'width': width, 'height': x}, {'width': width, 'height': y}]


def divide_list(l, bindings, types):
    result = [[], []]
    divide_type = bindings['element']
    divide = divide_type['_divide']
    
    for item in l:
        if isinstance(item, list):
            divisions = divide_list(item, bindings, types)
        else:
            divisions = divide(item, divide_type, types)

        result[0].append(divisions[0])
        result[1].append(divisions[1])

    return result


def replace(old_value, new_value, bindings, types):
    return new_value


def serialize_string(s, bindings, types):
    return f'"{s}"'

def deserialize_string(s, bindings, types):
    if s[0] != '"' or s[-1] != '"':
        raise Exception(f'deserializing str which requires double quotes: {s}')
    return s[1:-1]


def to_string(value, bindings, types):
    return str(value)

def deserialize_int(i, bindings, types):
    return int(i)

def deserialize_float(i, bindings, types):
    return float(i)

def evaluate(code, bindings, types):
    return eval(code)


# TODO: make these work
def apply_tree(current, update, bindings, types):
    if isinstance(update, dict):
        if current is None:
            current = {}
        for key, branch in update.items():
            if key == '_add':
                current.update(branch)
            elif key == '_remove':
                current = remove_path(current, branch)
            else:
                current[key] = apply_tree(
                    current.get(key),
                    branch,
                    bindings,
                    types)

        return current
    else:
        leaf_type = bindings['leaf']
        if current is None:
            current = types.default(leaf_type)
        return types.apply(leaf_type, current, update)


def divide_tree(tree, bindings, types):
    result = [{}, {}]
    # get the type of the values for this dict
    divide_type = bindings['leaf']
    divide_function = divide_type['_divide']
    # divide_function = types.registry_registry.type_attribute(
    #     divide_type,
    #     '_divide')

    for key, value in tree:
        if isinstance(value, dict):
            divisions = divide_tree(value)
        else:
            divisions = types.divide(divide_type, value)

        result[0][key], result[1][key] = divisions

    return result

def serialize_tree(value, bindings, types):
    return value

def deserialize_tree(value, bindings, types):
    return value


def apply_dict(current, update, bindings, types):
    pass

def divide_dict(value, bindings, types):
    return value

def serialize_dict(value, bindings, types):
    return value

def deserialize_dict(value, bindings, types):
    return value


def apply_maybe(current, update, bindings, types):
    if current is None or update is None:
        return update
    else:
        value_type = bindings['value']
        return types.apply(value_type, current, update)

def divide_maybe(value, bindings):
    if value is None:
        return [None, None]
    else:
        pass

def serialize_maybe(value, bindings, types):
    if value is None:
        return NONE_SYMBOL
    else:
        value_type = bindings['value']
        return serialize(value_type, value)

def deserialize_maybe(encoded, bindings, types):
    if encoded == NONE_SYMBOL:
        return None
    else:
        value_type = bindings['value']
        return deserialize(value_type, encoded)


# TODO: deal with all the different unit types
def apply_units(current, update, bindings, types):
    return current + update

def serialize_units(value, bindings, types):
    return str(value)

def deserialize_units(encoded, bindings, types):
    return units(encoded)

def divide_units(value, bindings, types):
    return [value, value]


# TODO: implement edge handling
def apply_edge(current, update, bindings, types):
    return current + update

def serialize_edge(value, bindings, types):
    return str(value)

def deserialize_edge(encoded, bindings, types):
    return eval(encoded)

def divide_edge(value, bindings, types):
    return [value, value]


def register_units(types, units):
    for unit_name in units._units:
        try:
            unit = getattr(units, unit_name)
        except:
            # print(f'no unit named {unit_name}')
            continue

        dimensionality = unit.dimensionality
        type_key = render_units_type(dimensionality)
        if types.type_registry.access(type_key) is None:
            types.type_registry.register(type_key, {
                '_default': '',
                '_apply': 'apply_units',
                '_serialize': 'serialize_units',
                '_deserialize': 'deserialize_units',
                '_divide': 'divide_units',
                '_description': 'type to represent values with scientific units'})


base_type_library = {
    # abstract number type
    'number': {
        '_type': 'number',
        '_apply': 'accumulate',
        '_serialize': 'to_string',
        '_description': 'abstract base type for numbers'},

    'int': {
        '_type': 'int',
        '_default': '0',
        # inherit _apply and _serialize from number type
        '_deserialize': 'deserialize_int',
        '_divide': 'divide_int',
        '_description': '64-bit integer',
        '_super': 'number',},

    'float': {
        '_type': 'float',
        '_default': '0.0',
        '_deserialize': 'float',
        '_divide': 'divide_float',
        '_description': '64-bit floating point precision number',
        '_super': 'number',}, 

    'string': {
        '_type': 'string',
        '_default': '""',
        '_apply': 'replace',
        '_serialize': 'serialize_string',
        '_deserialize': 'deserialize_string',
        '_divide': 'divide_int',
        '_description': '64-bit integer'},

    'list': {
        '_type': 'list',
        '_default': '[]',
        '_apply': 'concatenate',
        '_serialize': 'to_string',
        '_deserialize': 'evaluate',
        '_divide': 'divide_list',
        '_type_parameters': ['element'],
        '_description': 'general list type (or sublists)'},

    'tree': {
        '_type': 'tree',
        '_default': '{}',
        '_apply': 'apply_tree',
        '_serialize': 'serialize_tree',
        '_deserialize': 'deserialize_tree',
        '_divide': 'divide_tree',
        '_type_parameters': ['leaf'],
        '_description': 'mapping from str to some type (or nested dicts)'},

    'dict': {
        '_type': 'dict',
        '_default': '{}',
        '_apply': 'apply_dict',
        '_serialize': 'serialize_dict',
        '_deserialize': 'deserialize_dict',
        '_divide': 'divide_dict',
        # TODO: create assignable type parameters?
        '_type_parameters': ['key', 'value'],
        '_description': 'mapping from keys of any type to values of any type'},

    # TODO: add native numpy array type
    'array': {
        '_type': 'array',
        '_type_parameters': ['shape', 'element']},

    'maybe': {
        '_type': 'maybe',
        '_default': 'None',
        '_apply': 'apply_maybe',
        '_serialize': 'serialize_maybe',
        '_deserialize': 'deserialize_maybe',
        '_divide': 'divide_maybe',
        '_type_parameters': ['value'],
        '_description': 'type to represent values that could be empty'},

    'edge': {
        # TODO: do we need to have defaults informed by type parameters?
        '_type': 'edge',
        '_default': '{"wires": {}}',
        '_apply': 'apply_edge',
        '_serialize': 'serialize_edge',
        '_deserialize': 'deserialize_edge',
        '_divide': 'divide_edge',
        '_type_parameters': ['ports'],
        '_description': 'hyperedges in the bigraph, with ports as a type parameter',
        'wires': 'tree[list[string]]'}}


def register_base_types(types):

    # validate the function registered is of the right type?
    types.apply_registry.register('accumulate', accumulate)
    types.apply_registry.register('concatenate', concatenate)
    types.apply_registry.register('replace', replace)
    types.apply_registry.register('apply_tree', apply_tree)
    types.apply_registry.register('apply_dict', apply_dict)
    types.apply_registry.register('apply_maybe', apply_maybe)
    types.apply_registry.register('apply_units', apply_units)
    types.apply_registry.register('apply_edge', apply_edge)

    types.divide_registry.register('divide_float', divide_float)
    types.divide_registry.register('divide_int', divide_int)
    types.divide_registry.register('divide_longest', divide_longest)
    types.divide_registry.register('divide_list', divide_list)
    types.divide_registry.register('divide_tree', divide_tree)
    types.divide_registry.register('divide_dict', divide_dict)
    types.divide_registry.register('divide_maybe', divide_maybe)
    types.divide_registry.register('divide_units', divide_units)
    types.divide_registry.register('divide_edge', divide_edge)

    types.serialize_registry.register('serialize_string', serialize_string)
    types.serialize_registry.register('to_string', to_string)
    types.serialize_registry.register('serialize_tree', serialize_tree)
    types.serialize_registry.register('serialize_dict', serialize_dict)
    types.serialize_registry.register('serialize_maybe', serialize_maybe)
    types.serialize_registry.register('serialize_units', serialize_units)
    types.serialize_registry.register('serialize_edge', serialize_edge)

    types.deserialize_registry.register('float', deserialize_float)
    types.deserialize_registry.register('deserialize_int', deserialize_int)
    types.deserialize_registry.register('deserialize_string', deserialize_string)
    types.deserialize_registry.register('evaluate', evaluate)
    types.deserialize_registry.register('deserialize_tree', deserialize_tree)
    types.deserialize_registry.register('deserialize_dict', deserialize_dict)
    types.deserialize_registry.register('deserialize_maybe', deserialize_maybe)
    types.deserialize_registry.register('deserialize_units', deserialize_units)
    types.deserialize_registry.register('deserialize_edge', deserialize_edge)

    types.type_registry.register_multiple(base_type_library)
    register_units(types, units)

    return types


def schema_zoo():
    mitochondria_schema = {
        'mitochondria': {
            'volume': {'_type': 'float'},
            'membrane': {
                'surface_proteins': {'_type': 'tree[protein]'},
                'potential': {'_type': 'microvolts'}},
            'mass': {'_type': 'membrane?'},
        }
    }

    cytoplasm_schema = {
        'cytoplasm': {
            'mitochondria': {'_type': 'tree[mitochondria]'},
            'proteins': {'_type': 'tree[mitochondria]'},
            'nucleus': {'_type': 'tree[mitochondria]'},
            'transcripts': {'_type': 'tree[mitochondria]'},
        }
    }

    cell_schema = {
        'cell': {
            'shape': {'_type': 'mesh'},
            'volume': {'_type': 'mL'},
            'temperature': {'_type': 'K'},
        }
    }

    cell_composite = {
        'environment': {
            'outer_shape': {
                '_type': 'mesh', '_value': []},
            'cellA': {
                'cytoplasm': {
                    'external_ions': {'_type': 'ions'},
                    'internal_ions': {'_type': 'ions'},
                    'other_ions': {'_type': {
                        '_default': 0.0,
                        '_apply': accumulate,
                        '_serialize': str,
                        '_deserialize': float,
                        '_divide': divide_float,
                        '_description': '64-bit floating point precision number'
                    }},
                    'electron_transport': {
                        '_type': 'process',
                        '_value': 'ElectronTransport',
                        '_ports': {
                            'external_ions': 'ions',
                            'internal_ions': 'ions'},
                        '_wires': {
                            'external_ions': ['..', 'external_ions'],
                            'internal_ions': ['..', 'internal_ions']}
                        }
                    },
                'inner_shape': {'_type': 'mesh', '_value': []},
                '_ports': {
                    'shape': 'mesh',
                    'volume': 'mL',
                    'temperature': 'K'
                },
                '_channel': {
                    'shape': ['inner_shape'],
                },
                '_wires': {
                    'shape': ['..', 'outer_shape']
                }
            }
        }
    }

    compose({
        'cell': {
            'membrane': cell_schema,
            'cytoplasm': cytoplasm_schema
        }
    }, {
        
    })


def test_cube(base_types):
    cube_schema = {
        'shape': {
            '_type': 'shape',
            '_description': 'abstract shape type'},
        
        'rectangle': {
            '_type': 'rectangle',
            '_divide': 'divide_longest',
            '_description': 'a two-dimensional value',
            '_super': 'shape',
            'width': {'_type': 'int'},
            'height': {'_type': 'int'},
        },
        
        # cannot override existing keys unless it is of a subtype
        'cube': {
            '_type': 'cube',
            '_super': 'rectangle',
            'depth': {'_type': 'int'},
        },
    }

    base_types.type_registry.register_multiple(
        cube_schema)

    return base_types


@pytest.fixture
def base_types():
    return SchemaTypes()


@pytest.fixture
def cube_types(base_types):
    return test_cube(base_types)


def test_generate_default(cube_types):
    int_default = cube_types.default(
        {'_type': 'int'}
    )

    assert int_default == 0

    cube_default = cube_types.default(
        {'_type': 'cube'})

    assert 'width' in cube_default
    assert 'height' in cube_default
    assert 'depth' in cube_default

    nested_default = cube_types.default(
        {'a': 'int',
         'b': {
             'c': 'float',
             'd': 'cube'},
         'e': 'string'})

    assert nested_default['b']['d']['width'] == 0


def test_apply_update(cube_types):
    schema = {'_type': 'cube'}
    state = {
        'width': 11,
        'height': 13,
        'depth': 44,
    }
    update = {
        'depth': -5
    }

    new_state = cube_types.apply(
        schema,
        state,
        update
    )

    assert new_state['width'] == 11
    assert new_state['depth'] == 39


def print_schema_validation(types, library, should_pass):
    for key, declaration in library.items():
        report = types.validate_schema(declaration)
        if len(report) == 0:
            message = f'valid schema: {key}'
            if should_pass:
                print(f'PASS: {message}')
                pprint.pprint(declaration)
            else:
                raise Exception(f'FAIL: {message}\n{declaration}\n{report}')
        else:
            message = f'invalid schema: {key}'
            if not should_pass:
                print(f'PASS: {message}')
                pprint.pprint(declaration)
            else:
                raise Exception(f'FAIL: {message}\n{declaration}\n{report}')


def test_validate_schema(base_types):
    # good schemas
    print_schema_validation(base_types, base_type_library, True)

    good = {
        'not quite int': {
            '_default': 0,
            '_apply': 'accumulate',
            '_serialize': 'to_string',
            '_deserialize': 'deserialize_int',
            '_description': '64-bit integer'
        },
        'ports match': {
            'a': {
                '_type': 'int',
                '_value': 2
            },
            'edge1': {
                '_type': 'edge[a:int]',
                # '_type': 'edge',
                # '_ports': {
                #     '1': {'_type': 'int'},
                # },
            }
        }
    }        

    # bad schemas
    bad = {
        'empty': None,
        'str?': 'not a schema',
        'branch is weird': {
            'left': {'_type': 'ogre'},
            'right': {'_default': 1, '_apply': 'accumulate'},
        },
    }

    # test for ports and wires mismatch

    print_schema_validation(base_types, good, True)
    print_schema_validation(base_types, bad, False)


def test_fill_int(base_types):
    test_schema = {
        '_type': 'int'
    }

    full_state = base_types.fill(test_schema)
    direct_state = base_types.fill('int')

    assert full_state == direct_state == 0


def test_fill_cube(cube_types):
    test_schema = {
        '_type': 'cube'
    }

    partial_state = {
        'height': 5,
    }

    full_state = cube_types.fill(
        test_schema,
        state=partial_state)

    assert 'width' in full_state
    assert 'height' in full_state
    assert 'depth' in full_state
    assert full_state['height'] == 5
    assert full_state['depth'] == 0


def test_fill_in_missing_nodes(base_types):
    test_schema = {
        'edge 1': {
            '_type': 'edge',
            '_ports': {
                'port A': 'float'}}}

    test_state = {
        'edge 1': {
            'wires': {
                'port A': ['a']}}}

    filled = base_types.fill(
        test_schema,
        test_state)

    assert filled == {
        'a': 0.0,
        'edge 1': {
            'wires': {
                'port A': ['a']}}}


def test_fill_from_parse(base_types):
    test_schema = {
        'edge 1': 'edge[port A:float]'}

    test_state = {
        'edge 1': {
            'wires': {
                'port A': ['a']}}}

    filled = base_types.fill(
        test_schema,
        test_state)

    assert filled == {
        'a': 0.0,
        'edge 1': {
            'wires': {
                'port A': ['a']}}}


# def test_fill_in_disconnected_port(base_types):
#     test_schema = {
#         'edge1': {
#             '_type': 'edge',
#             '_ports': {
#                 '1': {'_type': 'float'}}}}

#     test_state = {}


# def test_fill_type_mismatch(base_types):
#     test_schema = {
#         'a': {'_type': 'int', '_value': 2},
#         'edge1': {
#             '_type': 'edge',
#             '_ports': {
#                 '1': {'_type': 'float'},
#                 '2': {'_type': 'float'}},
#             'wires': {
#                 '1': ['..', 'a'],
#                 '2': ['a']},
#             'a': 5}}


# def test_edge_type_mismatch(base_types):
#     test_schema = {
#         'edge1': {
#             '_type': 'edge',
#             '_ports': {
#                 '1': {'_type': 'float'}},
#             'wires': {
#                 '1': ['..', 'a']}},
#         'edge2': {
#             '_type': 'edge',
#             '_ports': {
#                 '1': {'_type': 'int'}},
#             'wires': {
#                 '1': ['..', 'a']}}}


def test_establish_path(base_types):
    tree = {}
    destination = establish_path(
        tree,
        ('some',
         'where',
         'deep',
         'inside',
         'lives',
         'a',
         'tiny',
         'creature',
         'made',
         'of',
         'light'))

    assert tree['some']['where']['deep']['inside']['lives']['a']['tiny']['creature']['made']['of']['light'] == destination


def test_expected_schema(base_types):
    # equivalent to previous schema:

    # expected = {
    #     'store1': {
    #         'store1.1': {
    #             '_value': 1.1,
    #             '_type': 'float',
    #         },
    #         'store1.2': {
    #             '_value': 2,
    #             '_type': 'int',
    #         },
    #         'process1': {
    #             '_ports': {
    #                 'port1': {'_type': 'type'},
    #                 'port2': {'_type': 'type'},
    #             },
    #             '_wires': {
    #                 'port1': 'store1.1',
    #                 'port2': 'store1.2',
    #             }
    #         },
    #         'process2': {
    #             '_ports': {
    #                 'port1': {'_type': 'type'},
    #                 'port2': {'_type': 'type'},
    #             },
    #             '_wires': {
    #                 'port1': 'store1.1',
    #                 'port2': 'store1.2',
    #             }
    #         },
    #     },
    #     'process3': {
    #         '_wires': {
    #             'port1': 'store1',
    #         }
    #     }
    # }

    dual_process_schema = {
        'process1': 'edge[port1:float|port2:int]',
        'process2': {
            '_type': 'edge',
            '_ports': {
                'port1': 'float',
                'port2': 'int',
            },
        },
    }

    base_types.type_registry.register(
        'dual_process',
        dual_process_schema,
    )

    test_schema = {
        # 'store1': 'process1:edge[port1:float|port2:int]|process2[port1:float|port2:int]',
        'store1': 'dual_process',
        'process3': 'edge[dual_process]'}

    test_state = {
        'store1': {
            'process1': {
                'wires': {
                    'port1': ['store1.1'],
                    'port2': ['store1.2'],
                }
            },
            'process2': {
                'wires': {
                    'port1': ['store1.1'],
                    'port2': ['store1.2'],
                }
            }
        },
        'process3': {
            'wires': {
                'port1': ['store1'],
            }
        },
    }
    
    outcome = base_types.fill(test_schema, test_state)

    assert outcome == {
        'process3': {
            'wires': {
                'port1': ['store1']
            }
        },
        'store1': {
            'process1': {
                'wires': {
                    'port1': ['store1.1'],
                    'port2': ['store1.2']
                }
            },
            'process2': {
                'wires': {
                    'port1': ['store1.1'],
                    'port2': ['store1.2']
                }
            },
            'store1.1': 0.0,
            'store1.2': 0
        }
    }


def test_link_place(base_types):
    # TODO: this form is more fundamental than the compressed/inline dict form,
    #   and we should probably derive that from this form

    bigraph = {
        'nodes': {
            'v0': 'int',
            'v1': 'int',
            'v2': 'int',
            'v3': 'int',
            'v4': 'int',
            'v5': 'int',
            'e0': 'edge[e0-0:int|e0-1:int|e0-2:int]',
            'e1': {
                '_type': 'edge',
                '_ports': {
                    'e1-0': 'int',
                    'e2-0': 'int'}},
            'e2': {
                '_type': 'edge[e2-0:int|e2-1:int|e2-2:int]'}},

        'place': {
            'v0': None,
            'v1': 'v0',
            'v2': 'v0',
            'v3': 'v2',
            'v4': None,
            'v5': 'v4',
            'e0': None,
            'e1': None,
            'e2': None},

        'link': {
            'e0': {
                'e0-0': 'v0',
                'e0-1': 'v1',
                'e0-2': 'v4'},
            'e1': {
                'e1-0': 'v3',
                'e1-1': 'v1'},
            'e2': {
                'e2-0': 'v3',
                'e2-1': 'v4',
                'e2-2': 'v5'}},

        'state': {
            'v0': '1',
            'v1': '1',
            'v2': '2',
            'v3': '3',
            'v4': '5',
            'v5': '8',
            'e0': {
                'wires': {
                    'e0-0': 'v0',
                    'e0-1': 'v1',
                    'e0-2': 'v4'}},
            'e1': {
                'wires': {
                    'e1-0': 'v3',
                    'e1-1': 'v1'}},
            'e2': {
                'e2-0': 'v3',
                'e2-1': 'v4',
                'e2-2': 'v5'}}}

    placegraph = { # schema
        'v0': {
            'v1': int,
            'v2': {
                'v3': int}},
        'v4': {
            'v5': int},
        'e0': 'edge',
        'e1': 'edge',
        'e2': 'edge'}

    hypergraph = { # edges
        'e0': {
            'e0-0': 'v0',
            'e0-1': 'v1',
            'e0-2': 'v4'},
        'e1': {
            'e1-0': 'v3',
            'e1-1': 'v1'},
        'e2': {
            'e2-0': 'v3',
            'e2-1': 'v4',
            'e2-2': 'v5'}}

    merged = {
        'v0': {
            'v1': {},
            'v2': {
                'v3': {}}},
        'v4': {
            'v5': {}},
        'e0': {
            'wires': {
                'e0.0': ['v0'],
                'e0.1': ['v0', 'v1'],
                'e0.2': ['v4']}},
        'e1': {
            'wires': {
                'e0.0': ['v0', 'v2', 'v3'],
                'e0.1': ['v0', 'v1']}},
        'e2': {
            'wires': {
                'e0.0': ['v0', 'v2', 'v3'],
                'e0.1': ['v4'],
                'e0.2': ['v4', 'v5']}}}

    result = base_types.link_place(placegraph, hypergraph)
    # assert result == merged


def test_units(base_types):
    schema_length = {
        'distance': {'_type': 'length'}}

    state = {'distance': 11 * units.meter}
    update = {'distance': -5 * units.feet}

    new_state = base_types.apply(
        schema_length,
        state,
        update
    )

    assert new_state['distance'] == 9.476 * units.meter


def test_serialize_deserialize(cube_types):
    schema = {
        'edge1': {
            # '_type': 'edge[1:int|2:float|3:string|4:tree[int]]',
            '_type': 'edge',
            '_ports': {
                '1': 'int',
                '2': 'float',
                '3': 'string',
                '4': 'tree[int]'}},
        'a0': {
            'a0.0': 'int',
            'a0.1': 'float',
            'a0.2': {
                'a0.2.0': 'string'}},
        'a1': 'tree[int]'}

    instance = {
        'edge1': {
            'wires': {
                '1': ['a0', 'a0.0'],
                '2': ['a0', 'a0.1'],
                '3': ['a0', 'a0.2', 'a0.2.0'],
                '4': ['a1']}},
        'a1': {
            'branch1': {
                'branch2': 11,
                'branch3': 22},
            'branch4': 44}}
    
    instance = cube_types.fill(schema, instance)

    encoded = cube_types.serialize(schema, instance)
    decoded = cube_types.deserialize(schema, encoded)

    assert instance == decoded


# is this a lens?
def test_project(cube_types):
    schema = {
        'edge1': {
            # '_type': 'edge[1:int|2:float|3:string|4:tree[int]]',
            # '_type': 'edge',
            '_type': 'edge',
            '_ports': {
                '1': 'int',
                '2': 'float',
                '3': 'string',
                '4': 'tree[int]'}},
        'a0': {
            'a0.0': 'int',
            'a0.1': 'float',
            'a0.2': {
                'a0.2.0': 'string'}},
        'a1': 'tree[int]'}

    path_format = {
        '1': 'a0>a0.0',
        '2': 'a0>a0.1',
        '3': 'a0>a0.2>a0.2.0'}

    # TODO: support separate schema/instance, and 
    #   instances with '_type' and type parameter keys
    # TODO: support overriding various type methods
    instance = {
        'edge1': {
            'wires': {
                '1': ['a0', 'a0.0'],
                '2': ['a0', 'a0.1'],
                '3': ['a0', 'a0.2', 'a0.2.0'],
                '4': ['a1']}},
        'a1': {
            'branch1': {
                'branch2': 11,
                'branch3': 22},
            'branch4': 44}}

    instance = cube_types.fill(schema, instance)
    
    states = cube_types.project(
        schema,
        instance,
        ['edge1'])

    update = cube_types.invert(
        schema,
        instance,
        ['edge1'],
        states)

    assert update == {
        'a0': {
            'a0.0': 0,
            'a0.1': 0.0,
            'a0.2': {
                'a0.2.0': ''}},
        'a1': {
            'branch1': {
                'branch2': 11,
                'branch3': 22},
            'branch4': 44}}

    updated_instance = cube_types.apply(
        schema,
        instance,
        update)

    add_update = {
        '4': {
            'branch6': 111,
            'branch1': {
                '_add': {
                    'branch7': 4444},
                '_remove': ['branch2']},
            '_add': {
                'branch5': 55},
            '_remove': ['branch4']}}

    inverted_update = cube_types.invert(
        schema,
        instance,
        ['edge1'],
        add_update)

    modified_branch = cube_types.apply(
        schema,
        instance,
        inverted_update)

    assert modified_branch == {
        'a0': {
            'a0.0': 0,
            'a0.1': 0.0,
            'a0.2': {
                'a0.2.0': ''}},
        'a1': {
            'branch1': {
                'branch7': 4444,
                'branch3': 44},
            'branch5': 55,
            'branch6': 111},
        'edge1': {
            'wires': {
                '1': ['a0', 'a0.0'],
                '2': ['a0', 'a0.1'],
                '3': ['a0', 'a0.2', 'a0.2.0'],
                '4': ['a1']}}}


if __name__ == '__main__':
    types = SchemaTypes()

    test_cube(types)
    test_generate_default(types)
    test_apply_update(types)
    test_validate_schema(types)
    test_fill_int(types)
    test_fill_cube(types)
    test_establish_path(types)
    test_expected_schema(types)
    test_units(types)
    test_fill_in_missing_nodes(types)
    test_fill_from_parse(types)
    test_serialize_deserialize(types)
    test_project(types)
