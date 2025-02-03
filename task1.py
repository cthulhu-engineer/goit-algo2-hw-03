import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

def create_graph():
    G = nx.DiGraph()
    edges = [
        ('Terminal_1', 'Warehouse_1', 25), ('Terminal_1', 'Warehouse_2', 20), ('Terminal_1', 'Warehouse_3', 15),
        ('Terminal_2', 'Warehouse_3', 15), ('Terminal_2', 'Warehouse_4', 30), ('Terminal_2', 'Warehouse_2', 10),
        ('Warehouse_1', 'Shop_1', 15), ('Warehouse_1', 'Shop_2', 10), ('Warehouse_1', 'Shop_3', 20),
        ('Warehouse_2', 'Shop_4', 15), ('Warehouse_2', 'Shop_5', 10), ('Warehouse_2', 'Shop_6', 25),
        ('Warehouse_3', 'Shop_7', 20), ('Warehouse_3', 'Shop_8', 15), ('Warehouse_3', 'Shop_9', 10),
        ('Warehouse_4', 'Shop_10', 20), ('Warehouse_4', 'Shop_11', 10), ('Warehouse_4', 'Shop_12', 15),
        ('Warehouse_4', 'Shop_13', 5), ('Warehouse_4', 'Shop_14', 10),
    ]
    G.add_weighted_edges_from(edges)
    return G

def draw_graph(G):
    pos = {
        'Terminal_1': (-1, 0), 'Terminal_2': (1, 0),
        'Warehouse_1': (-2, 2), 'Warehouse_2': (2, 2), 'Warehouse_3': (-2, -2), 'Warehouse_4': (2, -2),
        'Shop_1': (-3, 4), 'Shop_2': (-2.5, 4), 'Shop_3': (-2, 4),
        'Shop_4': (1, 4), 'Shop_5': (1.5, 4), 'Shop_6': (2, 4),
        'Shop_7': (-3, -4), 'Shop_8': (-2.5, -4), 'Shop_9': (-2, -4),
        'Shop_10': (1, -4), 'Shop_11': (1.5, -4), 'Shop_12': (2, -4),
        'Shop_13': (2.5, -4), 'Shop_14': (3, -4),
    }
    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color="skyblue", font_size=12, font_weight="bold", arrows=True)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show()

def bfs(capacity, flow, source, sink, parent):
    visited = [False] * len(capacity)
    queue = deque([source])
    visited[source] = True
    while queue:
        node = queue.popleft()
        for neighbor, cap in enumerate(capacity[node]):
            if not visited[neighbor] and cap - flow[node][neighbor] > 0:
                parent[neighbor] = node
                visited[neighbor] = True
                if neighbor == sink:
                    return True
                queue.append(neighbor)
    return False

def edmonds_karp(capacity, source, sink):
    num_nodes = len(capacity)
    flow = [[0] * num_nodes for _ in range(num_nodes)]
    parent = [-1] * num_nodes
    max_flow = 0
    while bfs(capacity, flow, source, sink, parent):
        path_flow = float('inf')
        node = sink
        while node != source:
            path_flow = min(path_flow, capacity[parent[node]][node] - flow[parent[node]][node])
            node = parent[node]
        node = sink
        while node != source:
            prev = parent[node]
            flow[prev][node] += path_flow
            flow[node][prev] -= path_flow
            node = prev
        max_flow += path_flow
    return max_flow

def main():
    G = create_graph()
    draw_graph(G)
    capacity_matrix = [
        [0, 0, 25, 20, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 10, 15, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 15, 10, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 10, 25, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 15, 10, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 10, 15, 5, 10],
    ]
    sources = [0, 1]
    sinks = list(range(6, 17))
    print("Термінал\tМагазин\tФактичний потік (одиниць)")
    for s in sources:
        for i in sinks:
            terminal = f"Terminal_{s + 1}"
            shop = f"Shop_{i - 5}"
            flow = edmonds_karp(capacity_matrix, s, i)
            print(f"{terminal}\t{shop}\t{flow}")

if __name__ == "__main__":
    main()
