import re
from pydoc import locate
import inspect
import types


def serialize(obj):
    if (isinstance(obj, (int, bool, str, float, type(None), complex))):
        obj = serialize_single(obj)
    elif (isinstance(obj, (list, tuple, set, frozenset, bytes))):
        obj = serialize_list(obj)
    elif (isinstance(obj, dict)):
        obj = serialize_dict(obj)
    elif (inspect.isfunction(obj) or inspect.ismethod(obj) or isinstance(obj, types.LambdaType)):
        obj = serialize_func(obj)
    elif (inspect.iscode(obj)):
        obj = serialize_code(obj)
    elif (inspect.isclass(obj)):
        obj = ser_class_old(obj)
    elif (inspect.ismethoddescriptor(obj) or inspect.isbuiltin(obj)):
        obj = serialize_instance(obj)
    elif inspect.ismemberdescriptor(obj):
        obj = serialize_instance(obj)
    elif inspect.isgetsetdescriptor(obj):
        obj = serialize_instance(obj)
    elif isinstance(obj, type(type.__dict__)):
        obj = serialize_instance(obj)
    elif inspect.ismodule(obj):
        return serialize_module(obj)

    else:
        obj = serialize_object(obj)

        # obj = tuple((k, obj[k]) for k in obj)

    return obj

def serialize_single(obj):
    serialized = dict()
    serialized['type'] = re.findall('\'\w+\'', str(type(obj)))[0].replace('\'', '')
    serialized['value'] = obj

    return serialized

def serialize_list(obj):
    serialized = dict()
    serialized['type'] = re.findall('\'\w+\'', str(type(obj)))[0].replace('\'', '')
    serialized['value'] = [serialize(tmp) for tmp in obj]

    return serialized

def serialize_dict(obj):
    serialized = dict()
    serialized['type'] = 'dict'
    serialized['value'] = dict()
    # serialized['value'] = tuple([tuple([serialize(obj[i]), serealize(i)]) for i in obj])

    serialized['value'] = [[serialize(tmp), serialize(obj[tmp])] for tmp in obj]

    return serialized


def serialize_func(obj):
    mems = inspect.getmembers(obj)
    serialized = dict()
    serialized['type'] = str(type(obj))[8:-2]
    val = dict()

    for tmp in mems:
        if (tmp[0] in ['__code__', '__name__', '__defaults__']):
            val[tmp[0]] = (tmp[1])
        if tmp[0] == '__code__':
            co_names = tmp[1].__getattribute__('co_names')
            globs = obj.__getattribute__('__globals__')
            val['__globals__'] = dict()

            for tmp_co_names in co_names:
                if tmp_co_names == obj.__name__:
                    val['__globals__'][tmp_co_names] = obj.__name__
                elif not inspect.ismodule(tmp_co_names) \
                        and tmp_co_names in globs:
                    # and tmp_co_names not in __builtins__:
                    val['__globals__'][tmp_co_names] = globs[tmp_co_names]

    serialized['value'] = serialize(val)

    return serialized


def serialize_code(obj):
    if (str(type(obj))[8:-2] == 'NoneType'):
        return None

    mems = inspect.getmembers(obj)

    serialized = dict()
    serialized['type'] = str(type(obj))[8:-2]
    serialized['value'] = serialize({tmp[0]: tmp[1] for tmp in mems if not callable(tmp[1])})

    return serialized


def serialize_instance(obj):
    mems = inspect.getmembers(obj)

    serialized = dict()
    serialized['type'] = str(type(obj))[8:-2]
    serialized['value'] = serialize({tmp[0]: tmp[1] for tmp in mems if not callable(tmp[1])})

    return serialized


def ser_class_old(obj):
    serialized = dict()
    val = dict()

    serialized['type'] = 'class'
    val['__name__'] = obj.__name__
    members = inspect.getmembers(obj)

    for tmp in members:
        if tmp[0] not in ['__class__',
                          '__getattribute__',
                          '__new__',
                          '__setattr__']:
            val[tmp[0]] = tmp[1]
    serialized['value'] = serialize(val)

    return serialized


def serialize_object(obj):

    serialized = dict()
    serialized['type'] = 'object'
    serialized['value'] = serialize({'__object_type__': type(obj), '__fields__': obj.__dict__})

    return serialized


def serialize_module(obj):
    tmp = str(obj)
    serialized = {'type': types.get_type(obj), 'value': tmp[9:-13]}

    return serialized


def deserialize(obj):
    if (obj['type'] in ['int', 'float', 'bool', 'complex', 'str']):
        return deserialize_single(obj)
    if (obj['type'] in ['list', 'set', 'frozenset', 'tuple', 'bytes']):
        return deserialize_list(obj)
    if (obj['type'] == 'dict'):
        return deserialize_dict(obj)
    if (obj['type'] == 'object'):
        return deserialize_object(obj)
    if (obj['type'] == 'class'):
        return deserialize_class(obj)
    if (obj['type'] == 'function'):
        return deserialize_func(obj)
    if (obj['type'] == 'module'):
        return deserialize_module(obj)


def deserialize_single(obj):
    tmp_obj = locate(obj['type'])
    return tmp_obj(obj['value'])


def deserialize_list(obj):
    tmp_obj = locate(obj['type'])
    return tmp_obj([deserialize(tmp) for tmp in obj['value']])


def deserialize_dict(obj):
    return {deserialize(tmp[0]): deserialize(tmp[1]) for tmp in obj['value']}


# def deserialize_object(obj):
#     value = deserialize(obj['value'])
#     result = value['__object_type__'](**value['__fields__'])
#
#     for key, value in value['__fields__'].items():
#         result.key = value
#
#     return result
def deserialize_object(obj):
    value = deserialize(obj['value'])
    result = value['__object_type__'](**value['__fields__'])

    for key, field_value in value['__fields__'].items():
        setattr(result, key, field_value)

    return result

def deserialize_class(obj):
    class_dict = deserialize(obj['value'])
    name = class_dict['__name__']
    del class_dict['__name__']

    return type(name, (object,), class_dict)

code_args = [
    'co_argcount',
    'co_posonlyargcount',
    'co_kwonlyargcount',
    'co_nlocals',
    'co_stacksize',
    'co_flags',
    'co_code',
    'co_consts',
    'co_names',
    'co_varnames',
    'co_filename',
    'co_name',
    'co_firstlineno',
    'co_linetable',
    'co_freevars',
    'co_cellvars'
]

def deserialize_code(obj):
    objs = obj['value']['value']

    for tmp in objs:
        if tmp[0]['value'] == '__code__':
            args = deserialize(tmp[1]['value'])
            code_dict = dict()
            for arg in args:
                arg_val = args[arg]
                if arg != '__doc__':
                    code_dict[arg] = arg_val
            code_list = [0] * 16

            for name in code_dict:
                if (name == 'co_lnotab'):
                    continue
                code_list[code_args.index(name)] = code_dict[name]

            return types.CodeType(*code_list)


def deserialize_func(obj):
    res_dict = deserialize(obj['value'])
    res_dict['code'] = deserialize_code(obj)
    res_dict.pop('__code__')
    res_dict['globals'] = res_dict['__globals__']
    res_dict.pop('__globals__')
    res_dict['name'] = res_dict['__name__']
    res_dict.pop('__name__')
    res_dict['argdefs'] = res_dict['__defaults__']
    res_dict.pop('__defaults__')

    res = types.FunctionType(**res_dict)
    if res.__name__ in res.__getattribute__('__globals__'):
        res.__getattribute__('__globals__')[res.__name__] = res

    return res


def deserialize_module(obj):
    return __import__(obj['value'])


