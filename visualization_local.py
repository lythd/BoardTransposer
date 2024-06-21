#!/usr/bin/env python3

import json
import sys
from collections import OrderedDict
import graphviz

def visualize_json(json_data, title="JSON Structure"):
    """
    Visualize the structure of a JSON object using a tree-like representation.

    :param json_data: The JSON data to visualize
    :param title: The title of the visualization
    """
    dot = graphviz.Digraph(comment=title)

    def add_node(node_id, node_value):
        if isinstance(node_value, dict):
            dot.node(node_id, "{}".format(node_value.keys()))
            for key, value in node_value.items():
                child_id = "{}_{}".format(node_id, key)
                dot.edge(node_id, child_id)
                add_node(child_id, value)
        elif isinstance(node_value, list):
            dot.node(node_id, "List[{}]".format(len(node_value)))
            for i, value in enumerate(node_value):
                child_id = "{}_{}".format(node_id, i)
                dot.edge(node_id, child_id)
                add_node(child_id, value)
        else:
            dot.node(node_id, "{}".format(node_value))

    root_id = "root"
    add_node(root_id, json_data)

    dot.format = "png"
    dot.render("json_structure", view=True)

# Visualize the JSON structure
def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = input("Enter the JSON file path: ")
    with open(filename) as f:
        data = json.load(f)
    visualize_json(data, title=f"{filename} Structure")

if __name__ == "__main__":
    main()
