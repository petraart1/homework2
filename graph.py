import json
import os
import xml.etree.ElementTree as ET
from graphviz import Digraph


def load_config(config_path):
    with open(config_path, 'r') as file:
        return json.load(file)


def parse_dependencies(file_path, max_depth):
    tree = ET.parse(file_path)
    root = tree.getroot()

    ns = {'mvn': 'http://maven.apache.org/POM/4.0.0'}

    dependencies = []
    for dependency in root.findall('.//mvn:dependency', ns):
        group_id = dependency.find('mvn:groupId', ns).text
        artifact_id = dependency.find('mvn:artifactId', ns).text
        version = dependency.find('mvn:version', ns).text if dependency.find('mvn:version', ns) is not None else "N/A"
        dependencies.append({
            'groupId': group_id,
            'artifactId': artifact_id,
            'version': version
        })

    return dependencies[:max_depth]


def create_graph(dependencies, package_name, output_file, graphviz_path):
    os.environ["PATH"] = f"{os.environ.get('PATH', '')}:{graphviz_path}"
    dot = Digraph(format='png', engine='dot')
    dot.node("Project", package_name, shape="box")

    for dep in dependencies:
        node_label = f"{dep['groupId']}:{dep['artifactId']}\n{dep['version']}"
        dot.node(node_label, node_label)
        dot.edge("Project", node_label)

    dot.render(output_file, view=False)