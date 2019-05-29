
class ConstError:

    class EnumError(Exception):
        pass

    class ConstSetError(Exception):
        pass


class EnumMeta(type):
    def __new__(cls, name, bases, attrs):
        choices = []
        message = {}
        for attr_str, attr_obj in attrs.items():
            if not attr_str.startswith('_'):
                assert attr_str.isupper(), f'options must be capitalized, wrong option: {attr_str}'
                if isinstance(attr_obj, tuple):
                    attrs[attr_str] = attr_obj[0]
                    choices.append(attr_obj)
                    message[attr_obj[0]] = attr_obj[1]
        if choices:
            choices.sort(key=lambda obj: obj[0])
            attrs['choices'] = choices
            attrs['message'] = message
        return type.__new__(cls, name, bases, attrs)


class BaseEnum(object, metaclass=EnumMeta):
    pass


class BaseConst:
    def __setattr__(self, name, value):
        raise ConstError.EnumError(f'Can\'t bind const instance attribute: {name}')


class ConstRegister:
    def __init__(self, const_obj):
        self.const_obj = const_obj

    def __call__(self, enum):
        setattr(self.const_obj.__class__, enum.__name__, enum)
        return enum
