import unittest
import json
from graph import *

class Tests(unittest.TestCase):

    def test_load_config(self):
        test_config = {
            "graphviz_program_path": "/usr/bin/dot",
            "package_name": "MyProject",
            "graph_image_path": "dependencies_graph.png",
            "max_depth": 2,
            "pom_file_path": "pom.xml"
        }
        with open("test_config.json", "w") as f:
            json.dump(test_config, f)

        config = load_config("test_config.json")
        self.assertEqual(config, test_config)

    def test_parse_dependencies(self):
        dependencies = parse_dependencies("test_pom.xml", max_depth=1)
        self.assertEqual(len(dependencies), 1)
        self.assertEqual(dependencies[0]['groupId'], 'org.example')
        self.assertEqual(dependencies[0]['artifactId'], 'example-artifact')
        self.assertEqual(dependencies[0]['version'], '1.0.0')

    def test_create_graph(self):
        dependencies = [
            {'groupId': 'org.example', 'artifactId': 'example-artifact', 'version': '1.0.0'},
            {'groupId': 'com.test', 'artifactId': 'test-artifact', 'version': 'N/A'}
        ]
        create_graph(dependencies, "MyProject", "test_graph", "/usr/bin")
        self.assertTrue(os.path.exists("test_graph.png"))