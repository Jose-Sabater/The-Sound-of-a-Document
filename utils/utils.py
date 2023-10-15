import re
import ast
import tiktoken


def str_to_dict(s: str) -> dict:
    # Replace single quotes with double quotes for strings
    s = re.sub(r"'(.*?)'", r'"\1"', s)

    # Replace lowercase booleans with Python's capitalized booleans
    s = s.replace("true", "True").replace("false", "False")

    try:
        # Use literal_eval to evaluate the string as Python dictionary
        return ast.literal_eval(s)
    except (ValueError, SyntaxError):
        return {}


def replace_placeholders_in_dict(template_dict: dict, replacements: dict) -> dict:
    """Replace placeholders in a dictionary with provided values."""
    updated_dict = template_dict.copy()

    # Iterate over items and replace placeholders in string values
    for key, value in updated_dict.items():
        if isinstance(value, list):
            updated_dict[key] = [item.format(**replacements) for item in value]
        elif isinstance(value, str):
            updated_dict[key] = value.format(**replacements)

    return updated_dict


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


# Try

# string = """{
#     "Answer": "In June 2019, you were in Wuppertal, Germany.",
#     "Missing_information": false
# }"""

# print(str_to_dict(string))
# print(type(str_to_dict(string)["Missing_information"]))
