import json
from typing import Any


# ----------------------------------------------------------------------------------------
def describe(name, value: Any, level: int = 0) -> str:
    """
    Compose a description of a variable's type and its value.

    Args:
        name: Name of the variable.
        value: Value of the variable.
        level: Indents output according to depth of recursion.
    """

    value_type = "%s.%s" % (type(value).__module__, type(value).__name__)

    if isinstance(value, dict):
        try:
            str_value = "\n" + json.dumps(value, indent=4)
        except TypeError:
            lines = []
            prefix = "\n" + ("." * (level * 2))
            # level += 1
            for index, item in value.items():
                lines.append(describe(f"{name}[{index}]", item, level))
            str_value = "\n" + prefix.join(lines)

    elif isinstance(value, list):
        if len(value) == 0:
            str_value = "length 0"
        else:
            try:
                str_value = "\n" + json.dumps(value, indent=4)
            except TypeError:
                lines = []
                prefix = "\n" + ("." * (level * 2))
                # level += 1
                for index, item in enumerate(value):
                    lines.append(describe(f"{name}[{index}]", item, level))
                str_value = "\n" + prefix.join(lines)

    elif isinstance(value, bytes):
        str_value = "length %d" % (len(value))

    elif value_type in ["CellExecutionError", "traitlets.config.loader.Config"]:
        lines = []
        prefix = "\n" + ("." * (level * 2))
        # level += 1
        for index, item in value.__dict__.items():
            lines.append(describe(f"{name}[{index}]", item, level))
        str_value = "\n" + prefix.join(lines)

    else:
        str_value = str(value)

    return "%s is a %s %s" % (name, value_type, str_value)
