import networkx as nx
import matplotlib.pyplot as plt


class DependencyPlan:
    """
    Class to generate dependency plan for given edge list
    Edge List:
    edge_list = [
        ("Report 1", "Report 5"),
        ("Report 1", "Report 3"),
        ("Report 8", "Report 10"),
        ("Report 5", "Report 8"),
    ]
    Returns: Dependency Plan
        {
            'Report 1': 0,
            'Report 5': 1,
            'Report 3': 1,
            'Report 8': 2,
            'Report 10': 3
        }
    """

    def __init__(self, connected_edge_list, list_of_node=None):
        """
        constructor for DependencyPlan.
        edge_list: list of set(parent,child)
        """
        if list_of_node is None:
            list_of_node = []
        self.edge_list = connected_edge_list
        self.dependency_plan = []
        self.graph = nx.DiGraph()
        self.graph.add_edges_from(connected_edge_list)
        self.set_node(list_of_node)

    def set_node(self, list_of_node):
        """
        Function to add nodes to the graph
        list_of_node: list of nodes to add
        """
        for node in list_of_node:
            self.graph.add_node(node)

    def get_dependency_plan_order_zero(self):
        """
        Function with use NetworkX package to find the dependency between the given edge list and
        prepare execution order for zero
        return: dependency_plan - dict of dependency order plan
        """

        # Generate weakly connected components of Graph
        tree = 0
        for comp in nx.weakly_connected_components(self.graph):
            tree = tree + 1
            start_nodes = []
            for link_node in comp:
                start_nodes.append(link_node)
            weakly_dependency_plan = self.clean_dependencies(
                self.get_node_dependencies(self.graph, start_nodes))
            self.dependency_plan.append(weakly_dependency_plan)
        return self.dependency_plan

    @staticmethod
    def get_node_dependencies(graph: nx.DiGraph, start_nodes):
        """
        Function to find the dependency between nodes
        graph: networkx graph object
        start_nodes: list of nodes/edges
        return: List[set] shortest_path_length
        """
        nodes = [(x, 0) for x in start_nodes]
        shortest_path_length = None
        for node, depth in nodes:
            shortest_path_length = nx.shortest_path_length(
                graph, source=node)

            this_depth = depth - 1
            for pre_node in graph.predecessors(node):
                nodes.append((pre_node, this_depth))
        return shortest_path_length

    def clean_dependencies(self, dependencies):
        """
        Function to generate dependency plan for given list[set]
        dependencies: dict
        return: List[dict] final_execution_order
        """
        final_execution_order = None
        for node, order in dependencies.items():
            if order == 0:
                final_execution_order = {
                    "node": node,
                    "order": order,
                    "child": len(self.get_successors(node))
                }
        return final_execution_order

    def draw_dependency(self):
        """
        DEV-ONLY
        This function is used to debug or view the graph as a pictorial view
        dd = DependencyDetector(edge_list, node_list)
        dd.draw_dependency()
        """
        # Draw
        nodelist = self.graph.nodes()
        widths = nx.get_edge_attributes(self.graph, 'weight')
        colors = range(20)

        plt.figure(figsize=(12, 8))
        pos = nx.shell_layout(self.graph)  # spring_layout or shell_layout
        nodes = nx.draw_networkx_nodes(
            self.graph, pos, node_color='orange', alpha=0.7, node_size=1500)
        edges = nx.draw_networkx_edges(
            self.graph,
            pos,
            arrowstyle='simple',
            arrowsize=20,
            arrows=True,
            alpha=0.6,
            style='solid',
            width=1,
            node_size=1500,
            edge_color='red',
            # connectionstyle="arc3,rad=0.1"
        )

        nx.draw_networkx_labels(self.graph, pos, labels=dict(zip(nodelist, nodelist)),
                                font_color='black')
        plt.box(False)
        plt.show()

    def get_successors(self, node):
        """
        Function to find successors of a given node
        node: string - current node to find the successor
        return: list
        """
        results = set(self.graph.successors(node))
        return results

    def get_predecessor(self, node):
        """
        Function to find predecessor of a given node
        node: string - current node to find the predecessor
        return: list
        """
        results = set(self.graph.predecessors(node))
        return results

    def validate_successors(self, node, successors):
        """
        Function to validate successors of a node
        node: string - current node
        successors: string - successor of the node to validate
        Return: bool
        """
        results = self.graph.has_successor(node, successors)
        return results

    def validate_predecessor(self, node, predecessors):
        """
        Function to validate predecessor of a node
        node: string - current node
        predecessor: string - predecessor of the node to validate
        Return: bool
        """
        results = self.graph.has_predecessor(node, predecessors)
        return results

    def get_successors_of_successors(self, node):
        """
        Function to find successors of successors for a given node
        node: string - current node to find the successors
        return: list
        """
        results = set()
        for successor in self.graph.successors(node):
            results.update(self.graph.successors(successor))
        return results

    def get_predecessors_of_predecessors(self, node):
        """
        Function to find successors of successors for a given node
        node: string - current node to find the successors
        return: list
        """
        results = set()
        for predecessors in self.graph.predecessors(node):
            results.update(self.graph.predecessors(predecessors))
        return results

    def get_tree_count(self):
        trees = []
        for comp in nx.weakly_connected_components(self.graph):
            trees.append(comp)
        return len(trees)

    def find_root_node(self, child):
        parent = list(self.graph.predecessors(child))
        if len(parent) == 0:
            return child
        else:
            return self.find_root_node(parent[0])

    def find_leaf_node(self, parent):
        child = list(self.graph.successors(parent))
        if len(child) == 0:
            return parent
        else:
            return self.find_leaf_node(child[0])

    def get_degree(self):
        degree = self.graph.degree()
        return degree

    def get_in_degree(self, node):
        in_degree = self.graph.in_degree(node)
        return in_degree

    def get_out_degree(self, node):
        out_degree = self.graph.out_degree(node)
        return out_degree

    def get_edges_list(self):
        return self.graph.edges()

    def get_neighbors(self, node):
        """Return a list of nodes connected to node n. """
        return list(self.graph.neighbors(node))

    def get_connected_nodes(self, node):
        all_connected_nodes = []
        for nodes in self.get_successors(node):
            all_connected_nodes.append(nodes)
        for nodes in self.get_predecessor(node):
            all_connected_nodes.append(nodes)
        return all_connected_nodes


# # Parent, Child
# edge_list = [
#     ("Report 1", "Report 5"),
#     ("Report 1", "Report 3"),
#     ("Report 2", "Report 4"),
#     ("Report 4", "Report 6"),
#     ("Report 6", "Report 7"),
#     ("Report 7", "Report 9"),
#     ("Report 8", "Report 10"),
#     ("Report 5", "Report 8"),
#     ("Report 8", "Report 3")
# ]

# dd = DependencyPlan(edge_list)
# plan = dd.get_dependency_plan()
# dd.draw_dependency()
# print(plan)
# print(dd.successors("Report 6"))
# print(dd.successors_of_successors("Report 6"))
# print(dd.predecessor("Report 6"))
# print(dd.predecessors_of_predecessors("Report 6"))
# print('Trees: ', dd.get_tree_count())
# print('find_root_node: ', dd.find_root_node("Report 10"))
# print('find_leaf_node: ', dd.find_leaf_node("Report 5"))
# print("degree ", dd.degree())
# print("in_degree ", dd.in_degree("Report 8"))
# print("out_degree ", dd.out_degree("Report 8"))
# print("get_edges_list :", dd.get_edges_list())
# print("validate_successors: ", dd.validate_successors("Report 8", "Report 10"))
# print("validate_predecessor: ", dd.validate_predecessor("Report 10", "Report 8"))
# print("neighbors ", dd.neighbors("Report 8"))
# print("get_connected_nodes ", dd.get_connected_nodes("Report 8"))
