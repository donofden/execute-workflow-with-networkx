from dependency_plan import DependencyPlan

EDGE_LIST = [
    ["Report 1", "Report 5"],
    ["Report 1", "Report 3"],
    ["Report 2", "Report 4"],
    ["Report 4", "Report 6"],
    ["Report 6", "Report 7"],
    ["Report 7", "Report 9"],
    ["Report 8", "Report 10"],
    ["Report 5", "Report 8"],
    ["Report 8", "Report 3"]
]

NETWORKX_EDGE_LIST = [
    ("Report 1", "Report 5"),
    ("Report 1", "Report 3"),
    ("Report 2", "Report 4"),
    ("Report 4", "Report 6"),
    ("Report 6", "Report 7"),
    ("Report 7", "Report 9"),
    ("Report 8", "Report 10"),
    ("Report 5", "Report 8"),
    ("Report 8", "Report 3")
]

NODE_LIST = [
    "Report 1",
    "Report 2",
    "Report 3",
    "Report 4",
    "Report 5",
    "Report 6",
    "Report 7",
    "Report 8",
    "Report 9",
    "Report 10",
    "Report 11"
]


def test_dependency_plan():
    """
    Test dependency plan
    """
    expected_plan = [
        {
            "node": "Report 1",
            "child": 2,
            "order": 0
        },
        {
            "node": "Report 2",
            "child": 1,
            "order": 0
        },
        {
            'node': 'Report 11',
            "child": 0,
            'order': 0
        }
    ]

    dd_obj = DependencyPlan(EDGE_LIST, NODE_LIST)
    plan = dd_obj.get_dependency_plan_order_zero()
    assert plan == expected_plan


def test_get_successor():
    """
    Test Get successor nodes
    """
    expected_nodes = {"Report 5", "Report 3"}

    dd_obj = DependencyPlan(EDGE_LIST, NODE_LIST)
    nodes = dd_obj.get_successors("Report 1")
    assert nodes == expected_nodes


def test_get_predecessors():
    """
    Test Get predecessor nodes
    """
    expected_nodes = {"Report 1", "Report 8"}

    dd_obj = DependencyPlan(EDGE_LIST, NODE_LIST)
    nodes = dd_obj.get_predecessor("Report 3")
    assert nodes == expected_nodes


def test_validate_successor():
    """
    Test validate successor nodes
    """

    dd_obj = DependencyPlan(EDGE_LIST, NODE_LIST)
    result = dd_obj.validate_successors("Report 1", "Report 5")
    assert result is True


def test_invalid_successor():
    """
    Test invalid successor nodes
    """

    dd_obj = DependencyPlan(EDGE_LIST, NODE_LIST)
    result = dd_obj.validate_successors("Report 1", "Report 8")
    assert result is False


def test_validate_predecessors():
    """
    Test validate predecessor nodes
    """

    dd_obj = DependencyPlan(EDGE_LIST, NODE_LIST)
    result = dd_obj.validate_predecessor("Report 3", "Report 1")
    assert result is True


def test_invalid_predecessor():
    """
    Test invalid predecessor nodes
    """

    dd_obj = DependencyPlan(EDGE_LIST, NODE_LIST)
    result = dd_obj.validate_predecessor("Report 8", "Report 12")
    assert result is False


def test_get_successors_of_successor():
    """
    Test Get successors of successor
    """
    expected_nodes = {"Report 8"}

    dd_obj = DependencyPlan(EDGE_LIST, NODE_LIST)
    nodes = dd_obj.get_successors_of_successors("Report 1")
    assert nodes == expected_nodes


def test_get_predecessors_of_predecessor():
    """
    Test Get predecessors of predecessor
    """
    expected_nodes = {"Report 5"}

    dd_obj = DependencyPlan(EDGE_LIST, NODE_LIST)
    nodes = dd_obj.get_predecessors_of_predecessors("Report 3")
    assert nodes == expected_nodes


def test_get_tree_count():
    """
    Test Get Graph count
    """

    dd_obj = DependencyPlan(EDGE_LIST, NODE_LIST)
    nodes = dd_obj.get_tree_count()
    assert nodes == 3


def test_find_root_node():
    """
    Test find root node
    """

    dd_obj = DependencyPlan(EDGE_LIST, NODE_LIST)
    nodes = dd_obj.find_root_node("Report 10")
    assert nodes == "Report 1"


def test_find_leaf_node():
    """
    Test find leaf node
    """

    dd_obj = DependencyPlan(EDGE_LIST, NODE_LIST)
    nodes = dd_obj.find_leaf_node("Report 4")
    assert nodes == "Report 9"


def test_get_degree():
    """
    Test get node degree
    """
    expected_degree = {
        'Report 1': 2,
        'Report 5': 2,
        'Report 3': 2,
        'Report 2': 1,
        'Report 4': 2,
        'Report 6': 2,
        'Report 7': 2,
        'Report 9': 1,
        'Report 8': 3,
        'Report 10': 1,
        'Report 11': 0
    }
    dd_obj = DependencyPlan(EDGE_LIST, NODE_LIST)
    degrees = dd_obj.get_degree()
    assert dict(degrees) == expected_degree


def test_get_in_degree():
    """
    Test get in degree
    """

    dd_obj = DependencyPlan(EDGE_LIST, NODE_LIST)
    degree = dd_obj.get_in_degree("Report 3")
    assert degree == 2


def test_get_out_degree():
    """
    Test get out degree
    """

    dd_obj = DependencyPlan(EDGE_LIST, NODE_LIST)
    degree = dd_obj.get_out_degree("Report 8")
    assert degree == 2


def test_get_edge_list():
    """
    Test get edge list
    """

    dd_obj = DependencyPlan(EDGE_LIST, NODE_LIST)
    result = dd_obj.get_edges_list()
    assert sorted(list(result)) == sorted(NETWORKX_EDGE_LIST)


def test_graph_without_node_list():
    """
    Test graph without node list
    """

    dd_obj = DependencyPlan(EDGE_LIST)
    result = dd_obj.get_edges_list()
    assert sorted(list(result)) == sorted(NETWORKX_EDGE_LIST)


def test_get_neighbours():
    """
    Test get neighbour nodes
    """
    expected_nodes = ["Report 5", "Report 3"]
    dd_obj = DependencyPlan(EDGE_LIST, NODE_LIST)
    nodes = dd_obj.get_neighbors("Report 1")
    assert nodes == expected_nodes


def test_get_connected_nodes():
    """
    Test get connected nodes
    """
    expected_nodes = ["Report 5", "Report 3", "Report 10"]
    dd_obj = DependencyPlan(EDGE_LIST, NODE_LIST)
    nodes = dd_obj.get_connected_nodes("Report 8")
    assert sorted(nodes) == sorted(expected_nodes)
