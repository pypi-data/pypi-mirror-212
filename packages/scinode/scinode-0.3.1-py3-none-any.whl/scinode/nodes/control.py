from scinode.core.node import Node


class ScinodeIf(Node):
    identifier: str = "If"
    node_type: str = "Normal"
    catalog = "Control"

    def create_sockets(self):
        self.inputs.clear()
        self.outputs.clear()
        self.inputs.new("General", "Input")
        self.outputs.new("General", "Result")
        self.kwargs = ["Input"]

    def create_ctrl_sockets(self):
        self.ctrl_inputs.clear()
        self.ctrl_outputs.clear()
        socket = self.ctrl_inputs.new("General", "Entry")
        socket.link_limit = 1000
        socket = self.ctrl_inputs.new("General", "Back")
        socket.link_limit = 1000
        self.ctrl_outputs.new("General", "Exit")
        self.ctrl_outputs.new("General", "True")
        self.ctrl_outputs.new("General", "False")

    def get_executor(self):
        return {
            "path": "scinode.executors.controls.if_node",
            "name": "ScinodeIf",
            "type": "class",
        }


class ScinodeFor(Node):
    identifier: str = "For"
    node_type: str = "Normal"
    catalog = "Control"

    def create_sockets(self):
        self.inputs.clear()
        self.outputs.clear()
        self.inputs.new("General", "Input")
        self.outputs.new("General", "Result")
        self.kwargs = ["Input"]

    def create_ctrl_sockets(self):
        self.ctrl_inputs.clear()
        self.ctrl_outputs.clear()
        socket = self.ctrl_inputs.new("General", "Entry")
        socket.link_limit = 1000
        socket = self.ctrl_inputs.new("General", "Iter")
        socket.link_limit = 1000
        self.ctrl_outputs.new("General", "Exit")
        self.ctrl_outputs.new("General", "Loop")

    def get_executor(self):
        return {
            "path": "scinode.executors.controls.for_node",
            "name": "ScinodeFor",
            "type": "class",
        }


class ScinodeSwitch(Node):
    identifier: str = "Switch"
    node_type: str = "Switch"
    catalog = "Control"

    def create_sockets(self):
        self.inputs.clear()
        self.outputs.clear()
        self.inputs.new("General", "Input")
        self.inputs.new("General", "Switch")
        self.outputs.new("General", "Result")
        self.kwargs = ["Input", "Switch"]

    def get_executor(self):
        return {
            "path": "scinode.executors.controls.switch_node",
            "name": "ScinodeSwitch",
            "type": "class",
        }


class ScinodeUpdate(Node):
    identifier: str = "Update"
    node_type: str = "Update"
    catalog = "Control"

    def create_sockets(self):
        self.inputs.clear()
        self.outputs.clear()
        self.inputs.new("General", "Input")
        self.inputs.new("General", "Update")
        self.outputs.new("General", "Result")
        self.kwargs = ["Input", "Update"]

    def get_executor(self):
        return {
            "path": "scinode.executors.controls.update_node",
            "name": "ScinodeUpdate",
            "type": "class",
        }


class ScinodeScatter(Node):
    identifier = "Scatter"
    node_type = "Control"
    catalog = "Control"

    def create_properties(self):
        self.properties.new("String", "DataType", data={"default": "General"})

    def create_sockets(self):
        self.inputs.clear()
        self.outputs.clear()
        socket = self.inputs.new("General", "Input")
        socket.link_limit = 100
        self.outputs.new("General", "Result")
        self.kwargs = ["Input"]

    def create_ctrl_sockets(self):
        self.ctrl_inputs.clear()
        self.ctrl_outputs.clear()
        socket = self.ctrl_inputs.new("General", "Entry")
        socket.link_limit = 1000
        socket = self.ctrl_inputs.new("General", "Back")
        socket.link_limit = 1000
        self.ctrl_outputs.new("General", "Exit")
        self.ctrl_outputs.new("General", "Scatter")

    def get_executor(self):
        return {
            "path": "scinode.executors.controls.scatter_node",
            "name": "ScinodeScatter",
            "type": "class",
        }


node_list = [
    ScinodeIf,
    ScinodeFor,
    ScinodeSwitch,
    ScinodeUpdate,
    ScinodeScatter,
]
