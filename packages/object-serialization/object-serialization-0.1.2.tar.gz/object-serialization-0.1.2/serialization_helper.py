import importlib
import types
from collections.abc import Iterable


def serialize_function(func):
    #   Serialize the function's code object to dictionary
    serialized_globals = {}
    for name, value in func.__globals__.items():
        if name == func.__name__ and name in func.__code__.co_names:
            # recursive call will be changed to new instance of function
            serialized_globals[name] = ""
        elif name in func.__code__.co_names:
            serialized_globals[name] = serialize_all(value)

    closure = func.__closure__
    new_cl = []
    if isinstance(closure, Iterable):
        for cell in closure:
            if cell.cell_contents != func:
                new_cl.append(cell)
            else:
                new_cl.append(types.CellType(None))
        closure = tuple(new_cl)
    ser_closure = serialize_all(closure)

    serialized_func = {
        '.type': "function",
        'name': serialize_all(func.__name__),  # name of function
        'argcount': serialize_all(func.__code__.co_argcount),  # number of arguments
        'posonlyargcount': serialize_all(func.__code__.co_posonlyargcount),  # number of positional arguments
        'kwonlyargcount': serialize_all(func.__code__.co_kwonlyargcount),  # number of key arguments
        'nlocals': serialize_all(func.__code__.co_nlocals),  # number of locals
        'stacksize': serialize_all(func.__code__.co_stacksize),  # potential used stack size (not useful)
        'flags': serialize_all(func.__code__.co_flags),  # code state flags
        'code': serialize_all(func.__code__.co_code),  # code of function as bytecode
        'consts': serialize_all(func.__code__.co_consts),  # values of consts
        'names': serialize_all(func.__code__.co_names),  # names of globals and attributes in function code (includes functions)
        'varnames': serialize_all(func.__code__.co_varnames),  # names of variables
        'filename': serialize_all(func.__code__.co_filename),  # name of file (not necessary)
        'firstlineno': serialize_all(func.__code__.co_firstlineno),  # position in code (not necessary)
        'lnotab': serialize_all(func.__code__.co_lnotab),  # offset info for bytecode
        'freevars': serialize_all(func.__code__.co_freevars),  # vars used in internal functions
        'cellvars': serialize_all(func.__code__.co_cellvars),  # vars used in internal functions

        'globals': serialized_globals,  # only globals that used in function
        'argdefs': serialize_all(func.__defaults__),   # default values for function arguments
        'closure': ser_closure     # neccesary closure data for proper creation of functions
    }

    return serialized_func


def deserialize_function(serialized_func):
    # Deserialize the function's code object from dictionary
    deserialized_code = types.CodeType(
        deserialize_all(serialized_func['argcount']),
        deserialize_all(serialized_func['posonlyargcount']),
        deserialize_all(serialized_func['kwonlyargcount']),
        deserialize_all(serialized_func['nlocals']),
        deserialize_all(serialized_func['stacksize']),
        deserialize_all(serialized_func['flags']),
        deserialize_all(serialized_func['code']),
        deserialize_all(serialized_func['consts']),
        deserialize_all(serialized_func['names']),
        deserialize_all(serialized_func['varnames']),
        deserialize_all(serialized_func['filename']),
        deserialize_all(serialized_func['name']),
        deserialize_all(serialized_func['firstlineno']),
        deserialize_all(serialized_func['lnotab']),
        deserialize_all(serialized_func['freevars']),
        deserialize_all(serialized_func['cellvars']),
    )

    recursive = False
    for name, value in serialized_func['globals'].items():  # editing non-primitive globals
        if name == serialized_func['name']:
            recursive = True
        elif not isinstance(value, (int, float, str)):  # deserialization of the rest objects
            serialized_func['globals'][name] = deserialize_all(value)

    recursive_closure = False
    closure = deserialize_all(serialized_func['closure'])
    if closure is not None:
        for cell in closure:
            if cell.cell_contents is None:
                recursive_closure = True

    deserialized_func = types.FunctionType(
        deserialized_code,
        globals=serialized_func['globals'],
        name=deserialize_all(serialized_func['name']),
        argdefs=deserialize_all(serialized_func['argdefs']),
        closure=closure
    )


    if recursive_closure:
        new_cl = []
        for cell in deserialized_func.__closure__:
            if cell.cell_contents is not None:
                new_cl.append(cell)
            else:
                cell.cell_contents = deserialized_func


    if recursive:
        deserialized_func.__globals__[serialized_func['name']] = deserialized_func

    return deserialized_func


def serialize_class(target):
    # Serialize the class object to dictionary
    serialized_attrs = {}         # serialize attributes

    for name, value in target.__dict__.items():
        if name not in ("__dict__", "__weakref__", "__doc__"):
            # __dict__, __weakref__, __doc__ not needed for serialization
            serialized_attrs[name] = serialize_all(value)

    serialized_bases = []           # serialize base classes
    for value in target.__bases__:
        if value.__bases__ != ():        # exclude 'object' class
            serialized_bases.append(serialize_class(value))

    serialized_class = {
        '.type': "class",
        "name": target.__name__,
        "attrs": serialized_attrs,
        "bases": serialized_bases
    }
    return serialized_class


def deserialize_class(serialized_target):
    # Deserialize the class object from dictionary
    for name, value in serialized_target["attrs"].items():
        serialized_target["attrs"][name] = deserialize_all(value)

    for i, value in enumerate(serialized_target["bases"]):
        serialized_target["bases"][i] = deserialize_class(value)

    deserialized_class = type(serialized_target["name"],
                              tuple(serialized_target["bases"]),
                              serialized_target["attrs"])

    return deserialized_class


def serialize_object(obj):
    # Serialize object (as class with data) to dictionary
    serialized_dict = {}
    for name, value in obj.__dict__.items():
        serialized_dict[name] = serialize_all(value)

    serialized_obj = {
        ".type": 'object',
        "class": serialize_class(type(obj)),
        "dict": serialized_dict
    }
    return serialized_obj


def deserialize_object(serialized_obj):
    # Deserialize object from dictionary

    obj_class = deserialize_class(serialized_obj["class"])
    obj = obj_class.__new__(obj_class)

    for name, value in serialized_obj["dict"].items():
        serialized_obj["dict"][name] = deserialize_all(value)

    for name, value in serialized_obj["dict"].items():
        setattr(obj, name, value)
    return obj


def serialize_module(module):
    # Serialize module only by its name to dictionary

    serialized_module = {
        ".type": 'module',
        "name": module.__name__,
    }
    return serialized_module


def deserialize_module(serialized_module):
    # Deserialize module from dictionary (i. e import again by name)
    module = importlib.import_module(serialized_module['name'])
    return module


def serialize_all(obj):
    if isinstance(obj, (int, float, str, complex, type(None))):  # primitive globals
        return obj
    elif isinstance(obj, types.GeneratorType):           # generator serialization
        return serialize_generator(obj)
    elif isinstance(obj, property):           # property serialization
        return serialize_property(obj)
    elif isinstance(obj, staticmethod):           # staticmethod serialization
        return serialize_staticmethod(obj)
    elif isinstance(obj, classmethod):           # classmethod serialization
        return serialize_classmethod(obj)
    elif isinstance(obj, types.CellType):           # cell serialization
        return serialize_cell(obj)
    elif isinstance(obj, types.CodeType):           # code serialization
        return serialize_code(obj)
    elif isinstance(obj, Iterable):                 # collection serialization
        return serialize_collection(obj)
    elif isinstance(obj, types.ModuleType):  # module serialization
        return serialize_module(obj)
    elif isinstance(obj, type):           # class serialization
        return serialize_class(obj)
    elif callable(obj):                     # function serialization
        return serialize_function(obj)
    else:
        return serialize_object(obj)


def deserialize_all(obj):
    if isinstance(obj, (int, float, str, type(None))):
        return obj
    elif isinstance(obj, list) or obj['.type'] in ["bytes", "tuple", "dict", "set", "frozenset"]:
        return deserialize_collection(obj)
    elif obj['.type'] == "function":
        return deserialize_function(obj)
    elif obj['.type'] == "class":
        return deserialize_class(obj)
    elif obj['.type'] == "object":
        return deserialize_object(obj)
    elif obj['.type'] == "module":
        return deserialize_module(obj)
    elif obj['.type'] == "cell":
        return deserialize_cell(obj)
    elif obj['.type'] == "code":
        return deserialize_code(obj)
    elif obj['.type'] == "classmethod":
        return deserialize_classmethod(obj)
    elif obj['.type'] == "staticmethod":
        return deserialize_staticmethod(obj)
    elif obj['.type'] == "property":
        return deserialize_property(obj)
    elif obj['.type'] == "generator":
        return deserialize_generator(obj)
    else:
        raise Exception("Wrong deserializable object")


def serialize_collection(col):
    # Serialize collection as dictionary
    ser_col = []
    if isinstance(col, list):
        return [serialize_all(val) for val in col]
    elif isinstance(col, set):
        type = 'set'
        ser_col = [serialize_all(val) for val in col]
    elif isinstance(col, frozenset):
        type = 'frozenset'
        ser_col = [serialize_all(val) for val in col]
    elif isinstance(col, dict):
        type = 'dict'
        ser_col = [[serialize_all(key), serialize_all(val)] for key, val in col.items()]
    elif isinstance(col, tuple):
        type = 'tuple'
        ser_col = [serialize_all(val) for val in col]
    elif isinstance(col, bytes):
        type = 'bytes'
        ser_col = [serialize_all(val) for val in col]

    serialized_module = {
        ".type": type,
        "collection": ser_col,
    }
    return serialized_module


def deserialize_collection(serialized_col):
    # Deserialize collection as dictionary
    if isinstance(serialized_col, list):
        return [deserialize_all(val) for val in serialized_col]

    serialized_col['collection'] = deserialize_all(serialized_col['collection'])
    if serialized_col['.type'] == "set":
        return set(serialized_col['collection'])
    elif serialized_col['.type'] == "frozenset":
        return frozenset(serialized_col['collection'])
    elif serialized_col['.type'] == "dict":
        return dict(serialized_col['collection'])
    elif serialized_col['.type'] == "tuple":
        return tuple(serialized_col['collection'])
    elif serialized_col['.type'] == "bytes":
        return bytes(serialized_col['collection'])


def serialize_cell(cell):
    serialized_cell = {
        ".type": 'cell',
        "value": serialize_all(cell.cell_contents),
    }
    return serialized_cell


def deserialize_cell(ser_cell):
    return types.CellType(deserialize_all(ser_cell['value']))


def serialize_code(code):
    ser_code = {

        '.type': "code",
        'argcount': serialize_all(code.co_argcount),  # number of arguments
        'posonlyargcount': serialize_all(code.co_posonlyargcount),  # number of positional arguments
        'kwonlyargcount': serialize_all(code.co_kwonlyargcount),  # number of key arguments
        'nlocals': serialize_all(code.co_nlocals),  # number of locals
        'stacksize': serialize_all(code.co_stacksize),  # potential used stack size (not useful)
        'flags': serialize_all(code.co_flags),  # code state flags
        'code': serialize_all(code.co_code),  # code of function as bytecode
        'consts': serialize_all(code.co_consts),  # values of consts
        'names': serialize_all(code.co_names),
        # names of globals and attributes in function code (includes functions)
        'varnames': serialize_all(code.co_varnames),  # names of variables
        'filename': serialize_all(code.co_filename),  # name of file (not necessary)
        'firstlineno': serialize_all(code.co_firstlineno),  # position in code (not necessary)
        'lnotab': serialize_all(code.co_lnotab),  # offset info for bytecode
        'freevars': serialize_all(code.co_freevars),  # vars used in internal functions
        'cellvars': serialize_all(code.co_cellvars),  # vars used in internal functions
    }
    return ser_code

def deserialize_code(ser_code):
    deserialized_code = types.CodeType(
        deserialize_all(ser_code['argcount']),
        deserialize_all(ser_code['posonlyargcount']),
        deserialize_all(ser_code['kwonlyargcount']),
        deserialize_all(ser_code['nlocals']),
        deserialize_all(ser_code['stacksize']),
        deserialize_all(ser_code['flags']),
        deserialize_all(ser_code['code']),
        deserialize_all(ser_code['consts']),
        deserialize_all(ser_code['names']),
        deserialize_all(ser_code['varnames']),
        deserialize_all(ser_code['filename']),
        'code',
        deserialize_all(ser_code['firstlineno']),
        deserialize_all(ser_code['lnotab']),
        deserialize_all(ser_code['freevars']),
        deserialize_all(ser_code['cellvars']),
    )
    return deserialized_code


def serialize_classmethod(method):
    ser_method = {

        '.type': "classmethod",
        'function': serialize_all(method.__func__)
    }
    return ser_method


def deserialize_classmethod(ser_method):
    func = deserialize_all(ser_method['function'])
    func = classmethod(func)
    return func


def serialize_staticmethod(method):
    ser_method = {
        '.type': "staticmethod",
        'function': serialize_all(method.__func__)
    }
    return ser_method


def deserialize_staticmethod(ser_method):
    func = deserialize_all(ser_method['function'])
    func = staticmethod(func)
    return func


def serialize_property(prop):
    ser_method = {
        '.type': "property",
        'function': serialize_all(prop.fget)
    }
    return ser_method


def deserialize_property(ser_prop):
    func = deserialize_all(ser_prop['function'])
    func = property(func)
    return func


def serialize_generator(gen):
    ser_gen = {
        '.type': "generator",
        'collection': serialize_all(list(gen))
    }
    return ser_gen


def deserialize_generator(ser_gen):
    col = deserialize_all(ser_gen['collection'])
    gen = (x for x in col)
    return gen
