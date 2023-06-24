import pkg_resources
import networkx as nx
import matplotlib.pyplot as plt

# Create an empty directed graph
graph = nx.DiGraph()

# Get all installed packages and their dependencies
installed_packages = pkg_resources.working_set
for package in installed_packages:
    # Add the package as a node in the graph
    graph.add_node(package.key)

    # Get the package dependencies
    for requirement in package.requires():
        # Add an edge from the package to its dependency
        graph.add_edge(package.key, requirement.key)

# Visualize the dependency graph
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(graph, seed=42)
nx.draw_networkx(graph, pos, with_labels=True, node_size=500, font_size=8, node_color='lightblue', edge_color='gray')
plt.title("Dependency Graph")
plt.axis('off')
plt.show()
