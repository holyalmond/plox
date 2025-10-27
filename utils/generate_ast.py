import sys
from typing import List, TextIO

def define_type(f: TextIO, base_name: str, class_name: str, field_list: str):
    f.write("@dataclass\n")
    f.write(f"class {class_name}({base_name}):\n")
    # init fields
    fields = field_list.split(", ")
    for field in fields:
        name = field.split(" ")[1]
        type = field.split(" ")[0]
        f.write(f"\t{name}: {type}\n")
    f.write("\n")

def define_ast(output_file: str, base_name: str, types: List[str]):
    path: str = output_file
    with open(path, "w") as f:
        # imports
        f.write("from abc import ABC\n")
        f.write("from dataclasses import dataclass\n")
        f.write("from tokens import Token\n\n")

        f.write(f"class {base_name}(ABC):\n")
        f.write("\tpass\n\n")
        for type in types:
            class_name = type.split(":")[0].strip()
            fields = type.split(":")[1].strip()
            define_type(f, base_name, class_name, fields)

def generate_ast(*args: str):
    if len(args) != 1:
        print("Usage: generate_ast <output directory>", file=sys.stderr)
        sys.exit(64)
    output_file = args[0]
    define_ast(output_file, "Expr", (
        "Binary   : Expr left, Token operator, Expr right",
        "Grouping : Expr expression",
        "Literal  : object value",
        "Unary    : Token operator, Expr right"
    ))
    
def main():
    generate_ast("plox/expressions.py")

if __name__ == "__main__":
    main()