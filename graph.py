import xml.etree.ElementTree as ET
from graphviz import Digraph

def parse_dependencies(file_path):
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

    return dependencies

def create_graph(dependencies, output_file='dependencies_graph'):
    dot = Digraph(format='png', engine='dot')
    for dep in dependencies:
        node_label = f"{dep['groupId']}:{dep['artifactId']}\n{dep['version']}"
        dot.node(node_label, node_label)
        dot.edge("Project", node_label)

    # Добавляем корневой проект
    dot.node("Project", "Project", shape="box")

    # Сохраняем и выводим граф
    dot.render(output_file, view=True)

file_path = 'pom.xml'
dependencies = parse_dependencies(file_path)
create_graph(dependencies)
