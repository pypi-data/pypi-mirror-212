from enum import auto, EnumMeta, Enum


class CustomEnumMeta(EnumMeta):

    def __contains__(cls, item):
        return item in cls._value2member_map_


class HttpMethods(Enum, metaclass=CustomEnumMeta):
    GET = auto()
    HEAD = auto()
    POST = auto()
    PUT = auto()
    DELETE = auto()
    CONNECT = auto()
    OPTIONS = auto()
    TRACE = auto()
    PATCH = auto()
