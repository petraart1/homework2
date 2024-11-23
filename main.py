from graph import *
import json
import os


def main():
    config_path = "config.json"
    config = load_config(config_path)

    graphviz_path = config["graphviz_program_path"]
    package_name = config["package_name"]
    graph_image_path = config["graph_image_path"]
    max_depth = config["max_depth"]
    pom_file_path = config["pom_file_path"]

    dependencies = parse_dependencies(pom_file_path, max_depth)

    create_graph(dependencies, package_name, graph_image_path, graphviz_path)


if __name__ == "__main__":
    main()