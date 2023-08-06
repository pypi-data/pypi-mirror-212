from scinode.core.node import Node


class IntNode(Node):
    """Output a int value."""

    identifier = "Int"
    name = "Int"
    catalog = "Input"

    args = ["Int"]

    def create_properties(self):
        self.properties.new("Int", "Int", data={"default": 0})

    def create_sockets(self):
        self.outputs.new("Int", "Int")

    def get_executor(self):
        return {
            "path": "builtins",
            "name": "int",
            "type": "function",
        }


class FloatNode(Node):
    """Output a float value."""

    identifier = "Float"
    name = "Float"
    catalog = "Input"

    args = ["Float"]

    def create_properties(self):
        self.properties.new("Float", "Float", data={"default": 0.0})

    def create_sockets(self):
        self.outputs.new("Float", "Float")

    def get_executor(self):
        return {
            "path": "builtins",
            "name": "float",
            "type": "function",
        }


class BoolNode(Node):
    """Output a bool value."""

    identifier = "Bool"
    name = "Bool"
    catalog = "Input"

    args = ["Bool"]

    def create_properties(self):
        self.properties.new("Bool", "Bool", data={"default": True})

    def create_sockets(self):
        self.outputs.new("Bool", "Bool")

    def get_executor(self):
        return {
            "path": "builtins",
            "name": "bool",
            "type": "function",
        }


class StrNode(Node):
    """Output a string."""

    identifier = "String"
    name = "String"
    catalog = "Input"

    args = ["String"]

    def create_properties(self):
        self.properties.new("String", "String", data={"default": ""})

    def create_sockets(self):
        self.outputs.new("String", "String")

    def get_executor(self):
        return {
            "path": "builtins",
            "name": "str",
            "type": "function",
        }


class DictNode(Node):
    """Output an empty Dict value."""

    identifier = "Dict"
    name = "Dict"
    catalog = "Input"

    def create_properties(self):
        pass

    def create_sockets(self):
        self.outputs.new("BaseDict", "Dict")

    def get_executor(self):
        return {
            "path": "builtins",
            "name": "dict",
            "type": "function",
        }


class Getattr(Node):
    """The Getattr node sets the value of the attribute of an object.

    Executor:
        Python builtin function: getattr()

    Results:
        A pyhont object.

    Example:

    >>> att = nt.nodes.new("Getattr")
    >>> att.properties["Name"].value = "real"

    """

    identifier: str = "Getattr"
    node_type: str = "Normal"
    catalog = "Builtin"

    def create_properties(self):
        pass

    def create_sockets(self):
        self.inputs.clear()
        self.outputs.clear()
        self.inputs.new("General", "Source")
        inp = self.inputs.new("String", "Name")
        inp.property.value = "__class__"
        self.outputs.new("General", "Result")
        self.args = ["Source", "Name"]

    def get_executor(self):
        return {
            "path": "builtins",
            "name": "getattr",
            "type": "function",
        }


class Setattr(Node):
    """The Setattr node sets the value of the attribute of an object.

    Executor:
        Python builtin function: setattr()

    Results:
        A pyhont object.

    Example:

    >>> nt = NodeTree(name="test_setattr")
    >>> person1 = nt.nodes.new("TestPerson", "person1")
    >>> str1 = nt.nodes.new("TestString", "str1")
    >>> str1.properties["String"].value = "Peter"
    >>> att = nt.nodes.new("Setattr")
    >>> att.properties["Name"].value = "name"
    >>> nt.links.new(person1.outputs[0], att.inputs["Source"])
    >>> nt.links.new(str1.outputs[0], att.inputs["Value"])

    """

    identifier: str = "Setattr"
    node_type: str = "Normal"
    catalog = "Builtin"

    def create_properties(self):
        pass

    def create_sockets(self):
        self.inputs.clear()
        self.outputs.clear()
        self.inputs.new("General", "Source")
        inp = self.inputs.new("General", "Name")
        inp.property.value = "__class__"
        self.inputs.new("General", "Value")
        self.outputs.new("General", "Result")
        self.args = ["Source", "Name", "Value"]

    def get_executor(self):
        return {
            "path": "scinode.executors.python",
            "name": "setattr",
            "type": "function",
        }


class Getitem(Node):
    """The Getitem node suppors index lookups.

    Executor:
        Python builtin function: __getitem__()

    Results:
        A pyhont object.

    Example:

    >>> getitem1 = nt.nodes.new("Getitem", "getitem1")
    >>> arange1 = nt.nodes.new("ScinodeNumpy", "arange")
    >>> arange1.set({"function": "arange", "start": 1, "stop": 5, "step": 2})
    >>> nt.links.new(nt.nodes["power1"].outputs[0], getitem1.inputs["Source"])
    >>> nt.links.new(arange1.outputs[0], getitem1.inputs["Index"])
    """

    identifier: str = "Getitem"
    node_type: str = "Normal"
    catalog = "Builtin"

    def create_properties(self):
        pass

    def create_sockets(self):
        self.inputs.clear()
        self.outputs.clear()
        self.inputs.new("General", "Source")
        inp = self.inputs.new("General", "Index")
        inp.property.value = 0
        self.outputs.new("General", "Result")
        self.args = ["Source", "Index"]

    def get_executor(self):
        return {
            "path": "scinode.executors.python",
            "name": "getitem",
            "type": "function",
        }


class Setitem(Node):
    """The Setitem node is used for assigning a value to an item.

    Executor:
        Python builtin function: __setitem__()

    Results:
        A pyhont object.

    Example:

    >>> setitem1 = nt.nodes.new("Setitem", "setitem1")
    >>> arange1 = nt.nodes.new("ScinodeNumpy", "arange")
    >>> arange1.set({"function": "arange", "start": 1, "stop": 5, "step": 2})
    >>> linspace2 = nt.nodes.new("ScinodeNumpy", "linspace2")
    >>> linspace2.set({"function": "linspace", "start": 11, "stop": 15, "num": 2})
    >>> nt.links.new(nt.nodes["linspace1"].outputs[0], setitem1.inputs["Source"])
    >>> nt.links.new(arange1.outputs[0], setitem1.inputs["Index"])
    >>> nt.links.new(linspace2.outputs[0], setitem1.inputs["Value"])
    """

    identifier: str = "Setitem"
    node_type: str = "Normal"
    catalog = "Builtin"

    def create_properties(self):
        pass

    def create_sockets(self):
        self.inputs.clear()
        self.outputs.clear()
        self.inputs.new("General", "Source")
        inp = self.inputs.new("General", "Index")
        inp.property.value = 0
        self.inputs.new("General", "Value")
        self.outputs.new("General", "Result")
        self.args = ["Source", "Index", "Value"]

    def get_executor(self):
        return {
            "path": "scinode.executors.python",
            "name": "setitem",
            "type": "function",
        }


list_func_items = [
    ["List", "List", "List"],
    ["Append", "Append", "Append"],
    ["Extend", "Extend", "Extend"],
    ["Remove", "Remove", "Remove"],
    ["Index", "Index", "Index"],
    ["Count", "Count", "Count"],
    ["Insert", "Insert", "Insert"],
    ["Pop", "Pop", "Pop"],
    ["Reverse", "Reverse", "Reverse"],
]


class List(Node):
    """Append a value to a list.

    Executor:
        Python builtin function: list.append()

    Results:
        List.

    Example:

    """

    identifier: str = "List"
    node_type: str = "Normal"
    catalog = "Builtin"

    def create_properties(self):
        self.properties.new(
            "Enum",
            "function",
            data={
                "default": "List",
                "options": list_func_items,
                "update": self.create_sockets,
            },
        )

    def create_sockets(self):
        self.inputs.clear()
        self.outputs.clear()
        if self.properties["function"].value in ["List"]:
            self.inputs.new("General", "Input")
            self.kwargs = ["Input"]
        elif self.properties["function"].value in [
            "Append",
            "Extend",
            "Remove",
            "Index",
            "Count",
        ]:
            self.inputs.new("BaseList", "List")
            self.inputs.new("General", "Value")
            self.kwargs = ["List", "Value"]
        elif self.properties["function"].value in ["Insert"]:
            self.inputs.new("BaseList", "List")
            self.inputs.new("Int", "Index")
            self.inputs.new("General", "Value")
            self.kwargs = ["List", "Index", "Value"]
        elif self.properties["function"].value in ["Pop"]:
            self.inputs.new("BaseList", "List")
            self.inputs.new("Int", "Index")
            self.kwargs = ["List", "Index"]
        elif self.properties["function"].value in ["Reverse"]:
            self.inputs.new("BaseList", "List")
            self.kwargs = ["List"]
        else:
            self.inputs.new("BaseList", "List")
            self.kwargs = ["List"]
        self.outputs.new("General", "Result")

    def get_executor(self):
        return {
            "path": "scinode.executors.list",
            "name": self.properties["function"].value,
            "type": "class",
        }


operator_items = [
    ["+", "+", "+"],
    ["-", "-", "-"],
    ["*", "*", "*"],
    ["/", "/", "/"],
    ["%", "%", "%"],
    ["**", "**", "**"],
    ["//", "//", "//"],
    ["==", "==", "=="],
    ["!=", "!=", "!="],
    [">", ">", ">"],
    ["<", "<", "<"],
    [">=", ">=", ">="],
    ["<=", "<=", "<="],
]


class Operator(Node):
    """Operators are used to perform operations on variables and values."""

    identifier: str = "Operator"
    node_type: str = "Normal"
    catalog = "Builtin"

    def create_properties(self):
        self.properties.new(
            "Enum",
            "operator",
            data={
                "default": "==",
                "options": operator_items,
                "update": self.create_sockets,
            },
        )

    def create_sockets(self):
        self.inputs.clear()
        self.outputs.clear()
        self.inputs.new("General", "x")
        self.inputs.new("General", "y")
        self.outputs.new("General", "Result")
        self.args = ["x", "y"]
        self.kwargs = ["operator"]

    def get_executor(self):
        return {
            "path": "scinode.executors.python",
            "name": "operator",
            "type": "fucntion",
        }


node_list = [
    IntNode,
    FloatNode,
    BoolNode,
    StrNode,
    DictNode,
    Getattr,
    Setattr,
    Getitem,
    Setitem,
    List,
    Operator,
]
