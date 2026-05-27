from app.algorithms.astar import find_fastest_route_with_heuristic
from app.algorithms.balanced import find_balanced_route
from app.algorithms.bfs import find_min_transfer_route
from app.algorithms.dijkstra import find_fastest_route
from app.algorithms.graph import Edge, Graph, Location, StationNode


def demo_graph() -> tuple[Graph, dict[str, StationNode]]:
    stations = {
        "A": StationNode("A", "Aksaray", ("M1", "M2"), Location(0, 0)),
        "B": StationNode("B", "Bahcelievler", ("M1",), Location(2, 1)),
        "C": StationNode("C", "Cevizlibag", ("M1",), Location(5, 1)),
        "D": StationNode("D", "Demirkapi", ("M2",), Location(3, 4)),
        "E": StationNode("E", "Esenler", ("M2", "M3"), Location(6, 5)),
        "F": StationNode("F", "Fenertepe", ("M3",), Location(9, 6)),
    }
    graph: Graph = {station_id: [] for station_id in stations}

    def add(a: str, b: str, line: str, minutes: int) -> None:
        graph[a].append(Edge(b, line, minutes, 1.0))
        graph[b].append(Edge(a, line, minutes, 1.0))

    add("A", "B", "M1", 2)
    add("B", "C", "M1", 3)
    add("A", "D", "M2", 5)
    add("D", "E", "M2", 2)
    add("E", "F", "M3", 6)
    return graph, stations


def test_bfs_finds_min_transfer_route() -> None:
    graph, _ = demo_graph()

    route = find_min_transfer_route(graph, "A", "F")

    assert route is not None
    assert route.path == ["A", "D", "E", "F"]
    assert route.transfer_count == 1


def test_dijkstra_finds_fastest_route() -> None:
    graph, _ = demo_graph()

    route = find_fastest_route(graph, "A", "F")

    assert route is not None
    assert route.path == ["A", "D", "E", "F"]
    assert route.total_duration_minutes == 13


def test_astar_matches_dijkstra_cost() -> None:
    graph, stations = demo_graph()

    dijkstra_route = find_fastest_route(graph, "A", "F")
    astar_route = find_fastest_route_with_heuristic(graph, stations, "A", "F")

    assert astar_route is not None
    assert dijkstra_route is not None
    assert astar_route.total_duration_minutes == dijkstra_route.total_duration_minutes


def test_balanced_returns_route_with_transfer_count() -> None:
    graph, _ = demo_graph()

    route = find_balanced_route(graph, "A", "F")

    assert route is not None
    assert route.path == ["A", "D", "E", "F"]
    assert route.transfer_count == 1


def test_same_start_and_goal_returns_single_station() -> None:
    graph, _ = demo_graph()

    route = find_fastest_route(graph, "A", "A")

    assert route is not None
    assert route.path == ["A"]
    assert route.total_duration_minutes == 0


def test_disconnected_route_returns_none() -> None:
    graph, _ = demo_graph()
    graph["X"] = []

    route = find_fastest_route(graph, "A", "X")

    assert route is None
