import re

from regex import regex

from StrangeSerializerLab3.AdditionalFunctions import AdditionalFunctions
from StrangeSerializerLab3.StrangeJSON.parser import parse
from types import NoneType as nonetype




INF_LITERAL = str(1E1000)
NAN_LITERAL = str(1E1000 / 1E1000)

TRUE_LITERAL = "true"
FALSE_LITERAL = "false"

NULL_LITERAL = "null"

INT_PATTERN = fr"[+-]?\d+"
FLOAT_PATTERN = fr"(?:[+-]?\d+(?:\.\d+)?(?:e[+-]?\d+)?|[+-]?{INF_LITERAL}\b|{NAN_LITERAL}\b)"
BOOL_PATTERN = fr"({TRUE_LITERAL}|{FALSE_LITERAL})\b"
STRING_PATTERN = fr"\"(?:(?:\\\")|[^\"])*\""
NULL_PATTERN = fr"\b{NULL_LITERAL}\b"

ELEMENTARY_TYPES_PATTERN = fr"{FLOAT_PATTERN}|{INT_PATTERN}|{BOOL_PATTERN}|{STRING_PATTERN}|{NULL_PATTERN}"

# This regex use recursive statements to be able to capture nested lists and objects.
ARRAY_PATTERN = r"\[(?R)?(?:,(?R))*\]"
OBJECT_PATTERN = r"\{(?:(?R):(?R))?(?:,(?R):(?R))*\}"

VALUE_PATTERN = fr"\s*({ELEMENTARY_TYPES_PATTERN}|" + \
                fr"{ARRAY_PATTERN}|{OBJECT_PATTERN})\s*"


class StrangeJsonSerializer:
    @staticmethod
    def dump(obj, file_name):
        with open(file_name, 'w') as file:
            file.write(StrangeJsonSerializer.dumps(obj))

    @staticmethod
    def dumps(obj):
        obj = AdditionalFunctions.to_dict(obj)
        return StrangeJsonSerializer.__dumps_from_dict(obj)
        # return str(serialize(obj))

    @staticmethod
    def load(file_name):
        with open(file_name, 'r') as file:
            return StrangeJsonSerializer.loads(file.read())

    @staticmethod
    def loads(str_tmp):
        obj = StrangeJsonSerializer.__loads_to_dict(str_tmp)
        return AdditionalFunctions.from_dict(obj)
        # return deserialize(parse(str_tmp))

    @staticmethod
    def __loads_to_dict(string: str):
        string = string.strip()

        # Int
        match = re.fullmatch(INT_PATTERN, string)
        if match:
            return int(match.group(0))

        # Float
        match = re.fullmatch(FLOAT_PATTERN, string)
        if match:
            return float(match.group(0))

        # Bool
        match = re.fullmatch(BOOL_PATTERN, string)
        if match:
            return match.group(0) == TRUE_LITERAL

        # Str
        match = re.fullmatch(STRING_PATTERN, string)
        if match:
            ans = match.group(0)
            ans = StrangeJsonSerializer.__unmask_quotes(ans)
            return ans[1:-1]

        # None
        match = re.fullmatch(NULL_PATTERN, string)
        if match:
            return None

        # List
        if string[0] == '[' and string[-1] == ']':
            string = string[1:-1]
            matches = regex.findall(VALUE_PATTERN, string)
            return [StrangeJsonSerializer.__loads_to_dict(match[0]) for match in matches]

        # Dict
        if string[0] == '{' and string[-1] == '}':
            string = string[1:-1]
            matches = regex.findall(VALUE_PATTERN, string)

            # Variable matches will store key-value pairs in one row. Elements with
            # even indexes are keys, those with odd indexes are values.
            return {StrangeJsonSerializer.__loads_to_dict(matches[i][0]):
                        StrangeJsonSerializer.__loads_to_dict(matches[i + 1][0]) for i in range(0, len(matches), 2)}

        else:
            raise ValueError

    @staticmethod
    def __dumps_from_dict(obj) -> str:
        if type(obj) in (int, float):
            return str(obj)

        if type(obj) is bool:
            return TRUE_LITERAL if obj else FALSE_LITERAL

        if type(obj) is str:
            return '"' + StrangeJsonSerializer.__mask_quotes(obj) + '"'

        if type(obj) is nonetype:
            return NULL_LITERAL

        if type(obj) is list:
            return '[' + ", ".join([StrangeJsonSerializer.__dumps_from_dict(item) for item in obj]) + ']'

        if type(obj) is dict:
            return '{' + ", ".join([f"{StrangeJsonSerializer.__dumps_from_dict(item[0])}: "
                                    f"{StrangeJsonSerializer.__dumps_from_dict(item[1])}" for item in obj.items()]) + '}'
        else:
            raise ValueError

    # def loads(self, string: str):
    #     obj = self.__loads_to_dict(string)
    #     return AdditionalFunctions.from_dict(obj)

    @staticmethod
    def __mask_quotes(string: str) -> str:
        return string.replace('\\', "\\\\").replace('"', r"\"").replace("'", r"\'")

    @staticmethod
    def __unmask_quotes(string: str) -> str:
        return string.replace('\\\\', "\\").replace(r"\"", '"').replace(r"\'", "'")