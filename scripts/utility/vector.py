import math

from utility.path_function import Node


def add(nodeA: Node, nodeB: Node):
    return Node((nodeA.x + nodeB.x, nodeA.y + nodeB.y, nodeA.z + nodeB.z))


def subtract(nodeA: Node, nodeB: Node):
    return Node((nodeA.x - nodeB.x, nodeA.y - nodeB.y, nodeA.z - nodeB.z))


def multiply(scale: float, node: Node) -> Node:
    return Node((scale * node.x, scale * node.y, scale * node.z))


def divide(scale: float, node: Node) -> Node:
    return Node((node.x / scale, node.y / scale, node.z / scale))


def dot_product(nodeA: Node, nodeB: Node) -> float:
    return nodeA.x * nodeB.x + nodeA.y * nodeB.y + nodeA.z * nodeB.z


def norm(node: Node) -> float:
    return math.sqrt(dot_product(node, node))


def norms(nodes: list[Node]) -> float:
    return math.sqrt(sum([dot_product(node, node) for node in nodes]))
