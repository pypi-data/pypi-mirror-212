from Serialization504.serialiser import my_deserializer, my_serializer
import regex
from Serialization504.const import INT_REGULAR, BOOL_REGULAR, NONE_REGULAR, VALUE_REGULAR_EXPR, FLOAT_REGULAR

class serialiser_JSON:

    def dumps(self, obj):
        obj = my_serializer(obj)
        return self.check_value(obj)

    def dump(self, obj, file):
        file.write(self.dumps(obj))

    def check_value(self, value):
        if (isinstance(value, str)):
            return '"' + value.replace("\\", "\\\\"). \
                replace('"', "\""). \
                replace("'", "\'") + '"'

        elif (isinstance(value, (int, float, complex))):
            return str(value)

        elif (isinstance(value, bool)):
            return "true" if value else "false"

        elif (isinstance(value, list)):
            return "[" + ", ".join([self.check_value(val) for val in value]) + "]"

        if (isinstance(value, dict)):
            return "{" + ", ".join([f"{self.check_value(k)}: \
                                    {self.check_value(v)}" for k, v in value.items()]) + "}"

    def loads(self, string):
        # print(string, "\n\n")
        obj = self.find_elem(string)
        return my_deserializer(obj)

    def load(self, file):
        return self.loads(file.read())

    STR_REGULAR = r"\"(?:(?:\\\")|[^\"])*\""
    def find_elem(self, string):
        string = string.strip()

        match = regex.fullmatch(INT_REGULAR, string)
        if (match):
            return int(match.group(0))

        match = regex.fullmatch(self.STR_REGULAR, string)
        if (match):
            res = match.group(0)
            res = res.replace("\\\\", "\\"). \
                replace(r"\"", '"'). \
                replace(r"\'", "'")
            return res[1:-1]

        match = regex.fullmatch(FLOAT_REGULAR, string)
        if (match):
            return float(match.group(0))

        match = regex.fullmatch(BOOL_REGULAR, string)
        if (match):
            return match.group(0) == "true"

        match = regex.fullmatch(NONE_REGULAR, string)
        if (match):
            return None

        if (string.startswith("[") and string.endswith("]")):
            string = string[1:-1]
            # print("LIST", string)
            matches = regex.findall(VALUE_REGULAR_EXPR, string)
            return [self.find_elem(match[0]) for match in matches]

        if (string.startswith("{") and string.endswith("}")):
            string = string[1:-1]
            # print(string)
            matches = regex.findall(VALUE_REGULAR_EXPR, string)
            # print(len(matches), matches)
            return {self.find_elem(matches[i][0]):
                        self.find_elem(matches[i + 1][0])
                    for i in range(0, len(matches), 2)}