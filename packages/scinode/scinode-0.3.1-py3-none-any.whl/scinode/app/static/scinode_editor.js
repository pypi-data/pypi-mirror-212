class ScinodeEditor extends Rete.NodeEditor {

    constructor(id, container){
        super(id, container);
        this.name = 'NodeTree'
        this.meta = {
                    "worker_name": 'localhost',
                    "platform": "rete",
                    "parent": "",
                    "parent_node": "",
                    "scatter_node": "",
                    "scattered_label": "",
                };
        this.uuid = uuid4();
        console.log("uuid: " + this.uuid);
        this.state = 'CREATED'
        this.action = 'NONE'
    }

    // override the toJSON method
    toJSON() {
        var data = super.toJSON()
        data['name'] = this.name;
        data['uuid'] = this.uuid;
        data['metadata'] = this.meta,
        data['links'] = [];
        data['description'] = "";
        // save links
        // input and ouput are always paired, so we only need to save the input
        for (let i = 0; i < this.nodes.length; i++) {
            var node = this.nodes[i];
            // inputs
            for ( let [key, input] of node.inputs) {
                data["nodes"][node.id]["inputs"][key]["name"] = input.name;
                data["nodes"][node.id]["inputs"][key]["uuid"] = input.uuid;
                // data["nodes"][node.id]["inputs"][key]["node_uuid"] = node.uuid;
                data["nodes"][node.id]["inputs"][key]["links"] = [];
                // links
                for ( let i=0; i< input.connections.length; i++) {
                    var link = {};
                    link["from_node"] = input.connections[i].output.node.label;
                    link["from_socket"] = input.connections[i].output.name;
                    // link["from_socket_uuid"] = input.connections[i].output.uuid;
                    link["to_node"] = node.label;
                    link["to_socket"] = input.name;
                    // link["to_socket_uuid"] = input.uuid;
                    data["nodes"][node.id]["inputs"][key]["links"].push(link);
                }
            }
        }
        return data;
    }
}
