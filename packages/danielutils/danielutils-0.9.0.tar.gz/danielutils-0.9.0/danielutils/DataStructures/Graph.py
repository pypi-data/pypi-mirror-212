from typing import Optional, Generator
from .Queue import Queue
from .Node import MultiNode


class Graph:
    def __init__(self, nodes: Optional[list[MultiNode]] = None):
        self.nodes: list[MultiNode] = nodes if nodes is not None else []

    def add_node(self, node):
        self.nodes.append(node)

    def _extended_dfs(self) -> Generator:
        seen = set()
        enter_times = dict()
        exit_times = dict()
        travel_index = 1
        all_nodes = []

        def handle_node(node: MultiNode):
            nonlocal travel_index
            seen.add(node)
            all_nodes.append(node)
            yield node
            for subnode in node._children:
                if subnode not in seen:
                    travel_index += 1
                    enter_times[subnode] = travel_index
                    if subnode is not None:
                        yield from handle_node(subnode)
                    travel_index += 1
                    exit_times[subnode] = travel_index

        for node in self.nodes:
            if node not in seen:
                enter_times[node] = travel_index
                travel_index += 1
                yield from handle_node(node)
                travel_index += 1
                exit_times[node] = travel_index
        topological_order = sorted(
            all_nodes, key=lambda v: exit_times[v], reverse=True)
        return topological_order

    def dfs(self) -> Generator:
        yield from self._extended_dfs()

    def topological_sort(self) -> list:
        g = self._extended_dfs()
        try:
            while True:
                next(g)
        except StopIteration as e:
            return e.value

    def bfs(self) -> Generator:
        q = Queue()
        for node in self.nodes:
            q.push(node)
        seen = set()
        for node in q:
            if node not in seen:
                seen.add(node)
                yield node
                for child in node._children:
                    q.push(child)

    def __str__(self) -> str:
        tmp = []
        for n in self.dfs():
            tmp.append(f"\t{str(n)}")
        return "Graph(\n"+",\n".join(tmp)+"\n)"


__all__ = [
    "Graph"
]
