#!/bin/python3
import sys
import os
import json

class Element:
    def __init__(self, name: str):
        self.name : str = name
        self.children : list[Element] = []
        self.hascheckbox : bool = False
        self.ischecked : bool = False
        if (name.startswith("[x]") or name.startswith("[ ]")):
            self.hascheckbox = True
            if name.startswith("[x]"):
                self.ischecked = True
            else:
                self.ischecked = False
            self.name = name[3:].strip()

    def append(self, child : "Element") -> None:
        self.children.append(child)
        
    def setchecked(self, checked : bool) -> None:
        self.hascheckbox = True
        self.ischecked = checked

    def __str__(self) -> str:
        if self.hascheckbox:
            if len(self.children) == 0:
                return '{"' + self.name + '"' + ": " + str(self.children) + ', "checked":' + str(self.ischecked).lower() + "}"
            else:
                return '{"' + self.name + '"' + ": " + str(self.children) + ', "checked":' + str(self.ischecked).lower() + "}"

        else:
            if len(self.children) == 0:
                return '"' + self.name + '"'
            return '{"' + self.name + '"' + ": " + str(self.children) + "}"

    def __repr__(self) -> str:
        return str(self)


def parse(lines: list[str]) -> list[Element]:
    root = []
    for line in lines:
        if line.startswith("\n"):
            continue

        if not line.startswith("\t"):
            root.append(Element(line.strip()))
        else:
            # count tabs
            tabs = 0
            for char in line:
                if char == "\t":
                    tabs += 1
                else:
                    break
            elements = root
            for i in range(tabs - 1):
                elements = elements[-1].children

            elements[-1].append(Element(line.strip()))

    return root

def dump(obj: list[Element], level: int = 0) -> list[str]:
    lines = []

    for element in obj:
        # check if element has children
        if len(element.children) == 0:
            # check if element has checkbox
            if element.hascheckbox:
                if element.ischecked:
                    lines.append("\t" * level + "[x] " + element.name)
                else:
                    lines.append("\t" * level + "[ ] " + element.name)
            else:
                lines.append("\t" * level + element.name)
        else:
            # check if element has checkbox
            if element.hascheckbox:
                if element.ischecked:
                    lines.append("\t" * level + "[x] " + element.name)
                else:
                    lines.append("\t" * level + "[ ] " + element.name)
            else:
                lines.append("\t" * level + element.name)

            # recursively call the function for children elements
            lines += dump(element.children, level + 1)  

    return lines

def dumps(lines : list[str]) -> list[str]:
    def convert(obj) -> list[Element]:
        root = []

        if not isinstance(obj, list):
            obj = [obj]
        
        for item in obj:
            if isinstance(item, str):
                element = Element(item)
            if isinstance(item, dict):
                name = list(item.keys())[0]
                element = Element(name)
                children = item[name]
                element.children = convert(children)
                if "checked" in item.keys():
                    element.hascheckbox = True
                    element.ischecked = item["checked"]
            root.append(element)
        return root

    root = convert(json.loads("".join(lines)))
    data = dump(root)
    return data

                
def markdownify(obj: list[Element], title: str = "") -> list[str]:
    def get_element_and_level(elements : list[Element], level : int =0):
        flat_elements : list[(Element,int)] = []

        for element in elements:
            flat_elements.append((element, level))

            if len(element.children) > 0:
                flat_elements.extend(get_element_and_level(
                    element.children, level + 1))

        return flat_elements
    
    if title == "":
        for item in get_element_and_level(obj):
            if item[1] == 0:
                print()
                print("# " + item[0].name)
            elif item[1] == 1:
                print()
                print("## " + item[0].name)
            else:
                if item[0].hascheckbox:
                    print("\t" * (item[1] - 2) + "- [x] " + item[0].name) if item[0].ischecked else print ("\t" * (item[1] - 2) + "- [ ] " + item[0].name)
                else:
                    print("\t" * (item[1] - 2) + "- " + item[0].name)
    else:
        print()
        print ("# " + title.split(".")[0].strip().replace("_", " ").replace("-", " "))
        for item in get_element_and_level(obj):
            if item[1] == 0:
                print()
                print("## " + item[0].name)
            else:
                if item[0].hascheckbox:
                    print("\t" * (item[1] - 1) + "- [x] " + item[0].name) if item[0].ischecked else print ("\t" * (item[1] - 1) + "- [ ] " + item[0].name)
                else:
                    print("\t" * (item[1] - 1) + "- " + item[0].name)



def usage():
    print("Usage: vml [-d, -m] [file1.vml] [file2.vml] [file3.vml] ...")


def main():
    # check for arguments
    if len(sys.argv) == 1 and sys.stdin.isatty():
        usage()
        sys.exit(1)
    
    if len(sys.argv) > 1 and sys.stdin.isatty():
        if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            usage()
            sys.exit(0)
        if (sys.argv[1] == "-d" or sys.argv[1] == "--dump") and len(sys.argv) == 2:
            usage()
            sys.exit(1)
        if (sys.argv[1] == "-m" or sys.argv[1] == "--markdown") and len(sys.argv) == 2:
            usage()
            sys.exit(1)
            

    # get dashed arguments
    dashed_args = []
    for arg in sys.argv[1::]:
        if arg.startswith("-"):
            dashed_args.append(arg)
        else:
            break
        
    # dump logic
    if "-d" in dashed_args or "--dump" in dashed_args:
        if not sys.stdin.isatty():
            lines = sys.stdin.readlines()
            if len(lines) != 0:
                for line in dumps(lines):
                    print(line)

                sys.exit(0)

        for filename in sys.argv[1:]:
            if os.path.isfile(filename):
                with open(filename, "r") as f:
                    lines = f.readlines()

                for line in dumps(lines):
                    print(line)
        sys.exit(0)

    #markdownify logic
    elif "-m" in dashed_args or "--markdown" in dashed_args:
        if not sys.stdin.isatty():
            lines = sys.stdin.readlines()
            if len(lines) != 0:
                print(markdownify(parse(lines)))
                sys.exit(0)
            
        if len(sys.argv) == 3:
            if os.path.isfile(sys.argv[2]):
                with open(sys.argv[2], "r") as f:
                    lines = f.readlines()
                markdownify(parse(lines))
                sys.exit(0)

        for filename in sys.argv[1:]:
            if os.path.isfile(filename):
                with open(filename, "r") as f:
                    lines = f.readlines()
                markdownify(parse(lines), filename)
        sys.exit(0)
        
    #parse logic
    else:
        if not sys.stdin.isatty():
            lines = sys.stdin.readlines()
            if len(lines) != 0:
                print(parse(lines))
                sys.exit(0)

        for filename in sys.argv[1:]:
            if os.path.isfile(filename):
                with open(filename, "r") as f:
                    lines = f.readlines()
                print(parse(lines))
                


if __name__ == "__main__":
    main()
