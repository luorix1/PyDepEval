# # import pkg_resources
# # import networkx as nx
# # import matplotlib.pyplot as plt

# # # Create an empty directed graph
# # graph = nx.DiGraph()

# # # Get all installed packages and their dependencies
# # installed_packages = pkg_resources.working_set
# # for package in installed_packages:
# #     # Add the package as a node in the graph
# #     graph.add_node(package.key)

# #     # Get the package dependencies
# #     for requirement in package.requires():
# #         # Add an edge from the package to its dependency
# #         graph.add_edge(package.key, requirement.key)

# # # Check for circular imports
# # try:
# #     cycle = nx.find_cycle(graph, orientation='original')
# #     print("Circular dependency detected:")
# #     for edge in cycle:
# #         print(f"{edge[0]} -> {edge[1]}")
# # except nx.NetworkXNoCycle:
# #     print("No circular dependencies found.")

# # # Check for version conflicts
# # conflicts = []
# # for package in graph.nodes:
# #     requirements = pkg_resources.Requirement.parse(package)
# #     for dependent in pkg_resources.working_set:
# #         if dependent.key != package and requirements in dependent.requires():
# #             conflicts.append((package, dependent.key))

# # if conflicts:
# #     print("Version conflicts detected:")
# #     for conflict in conflicts:
# #         print(f"{conflict[0]} requires a different version of {conflict[1]}")

# import pkg_resources
# import networkx as nx

# # Create an empty directed graph
# graph = nx.DiGraph()

# # Get all installed packages and their dependencies
# installed_packages = pkg_resources.working_set
# for package in installed_packages:
#     # Add the package as a node in the graph
#     graph.add_node(package.key)

#     # Get the package dependencies
#     for requirement in package.requires():
#         # Add an edge from the package to its dependency
#         graph.add_edge(package.key, requirement.key)

# # Check for circular imports
# try:
#     cycle = nx.find_cycle(graph, orientation='original')
#     print("Circular dependency detected:")
#     for edge in cycle:
#         print(f"{edge[0]} -> {edge[1]}")
# except nx.NetworkXNoCycle:
#     print("No circular dependencies found.")

# conflicts = []
# for package in graph.nodes:
#     requirements = pkg_resources.Requirement.parse(package)
#     for dependent in pkg_resources.working_set:
#         if dependent.key != package and requirements in dependent.requires():

#             required_version = str(requirements.specifier)  # Convert to string
#             installed_version = dependent.version
#             conflicts.append((package, required_version, dependent.key, installed_version))

# if conflicts:
#     print("Version conflicts detected:")
#     for conflict in conflicts:
#         package, required_version, conflicting_package, installed_version = conflict
#         print(f"{package} requires {required_version} of {conflicting_package}, but {installed_version} is installed.")

import subprocess
import json
import networkx as nx
import matplotlib.pyplot as plt


def check_cyclic_dependencies(graph):
    try:
        cycle = nx.find_cycle(graph, orientation='original')
        print("Circular dependency detected:")
        for edge in cycle:
            print(f"{edge[0]} -> {edge[1]}")
    except nx.NetworkXNoCycle:
        print("No circular dependencies found.")


def check_version_conflicts(graph):
    conflicts = []
    for package in graph.nodes:
        try:
            installed_version = subprocess.check_output(["pip", "show", package]).decode().split("\n")[1].split(":")[1].strip()
        except subprocess.CalledProcessError:
            installed_version = "Not installed"
        for dependent in graph[package]:
            required_version = graph[package][dependent].get("required_version")
            if required_version and required_version != installed_version:
                conflicts.append((package, required_version, dependent, installed_version))
    if conflicts:
        print("Version conflicts detected:")
        for conflict in conflicts:
            package, required_version, conflicting_package, installed_version = conflict
            print(f"{package} requires {required_version} of {conflicting_package}, but {installed_version} is installed.")


def visualize_dependency_tree(graph):
    pos = nx.spring_layout(graph)
    plt.figure(figsize=(12, 8))
    nx.draw_networkx(graph, pos, with_labels=True, node_color='lightblue', edge_color='gray', alpha=0.7)
    plt.axis('off')
    plt.show()


def main():
    # Create an empty directed graph
    graph = nx.DiGraph()

    # Get the package information using pip
    pip_output = subprocess.check_output(["pip", "list", "--format=json"]).decode().strip()
    packages = json.loads(pip_output)

    # Build the dependency graph
    for package in packages:
        print(package["name"])
        package_name = package["name"]
        graph.add_node(package_name)

        if "requires_dist" in package:
            for dependency in package["requires_dist"]:
                dependency_parts = dependency.split(" ")
                dependency_name = dependency_parts[0]
                required_version = dependency_parts[1][1:-1]  # Strip the version specifier brackets
                graph.add_edge(package_name, dependency_name, required_version=required_version)

    # Check for cyclic dependencies
    check_cyclic_dependencies(graph)

    # Check for version conflicts
    check_version_conflicts(graph)

    # Visualize the dependency tree
    visualize_dependency_tree(graph)


if __name__ == "__main__":
    main()
