from scinode.core.node import Node


class TestSqrtPowerAdd(Node):

    identifier: str = "TestSqrtPowerAdd"
    name = "TestSqrtPowerAdd"
    catalog = "Test"
    node_type: str = "GROUP"

    def get_default_node_group(self):
        from scinode.nodetree import NodeTree

        nt = NodeTree(
            name=self.name,
            uuid=self.uuid,
            parent_node=self.uuid,
            worker_name=self.worker_name,
            type="NODE_GROUP",
        )
        sqrt1 = nt.nodes.new("TestSqrt", "sqrt1")
        power1 = nt.nodes.new("TestPower", "power1")
        add1 = nt.nodes.new("TestAdd", "add1")
        nt.links.new(sqrt1.outputs[0], add1.inputs[0])
        nt.links.new(power1.outputs[0], add1.inputs[1])
        nt.group_properties = [
            ("sqrt1", "t", "t1"),
            ("add1", "t", "t2"),
        ]
        nt.group_inputs = [
            ("sqrt1", "x", "x"),
            ("power1", "x", "y"),
        ]
        nt.group_outputs = [("add1", "Result", "Result")]
        return nt


class TestNestedSqrtAdd(Node):

    identifier: str = "TestNestedSqrtAdd"
    name = "TestNestedSqrtAdd"
    catalog = "Test"
    node_type: str = "GROUP"

    def get_default_node_group(self):
        from scinode.nodetree import NodeTree

        nt = NodeTree(
            name=self.name,
            uuid=self.uuid,
            parent_node=self.uuid,
            worker_name=self.worker_name,
            type="NODE_GROUP",
        )
        sqrt_power_add1 = nt.nodes.new("TestSqrtPowerAdd", "sqrt_power_add1")
        sqrt_power_add2 = nt.nodes.new("TestSqrtPowerAdd", "sqrt_power_add2")
        add1 = nt.nodes.new("TestAdd", "add1")
        nt.links.new(sqrt_power_add1.outputs[0], add1.inputs[0])
        nt.links.new(sqrt_power_add2.outputs[0], add1.inputs[1])
        nt.group_inputs = [("sqrt_power_add1", "x", "x"), ("sqrt_power_add2", "x", "y")]
        nt.group_outputs = [["add1", "Result", "Result"]]
        return nt


node_list = [
    TestSqrtPowerAdd,
    TestNestedSqrtAdd,
]
