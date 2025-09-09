import sys

# 文字列から「駅IDと距離のリスト」を抽出して、エッジのリストを返す
def read_input_from_string(s):
    edges = []
    # 複数の改行コードの書き方に対応
    s = s.replace("¥r¥n", "\n").replace("\\r\\n", "\n").replace("\r\n", "\n")
    for line in s.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = [p.strip() for p in line.split(",")]
        if len(parts) != 3:
            continue
        try:
            u, v, w = int(parts[0]), int(parts[1]), float(parts[2])
            edges.append((u, v, w))
        except ValueError:
            continue  # 数値に変換できない場合は無視
    return edges

# 隣接リスト形式でグラフを表現
def build_graph(edges):
    graph = {}
    for u, v, w in edges:
        if u not in graph:
            graph[u] = []
        graph[u].append((v, w))
    return graph

# DFSで最長片道経路を探索
def dfs(graph, node, visited, path, dist, result):
    visited.add(node)
    path.append(node)

    if dist > result['max_dist']:
        result['max_dist'] = dist
        result['max_path'] = path.copy()

    for neighbor, weight in graph.get(node, []):
        if neighbor not in visited:
            dfs(graph, neighbor, visited, path, dist + weight, result)

    visited.remove(node)
    path.pop()

if __name__ == "__main__":
    # 標準入力全体を読み込む（複数行対応）
    input_str = sys.stdin.read()
    edges = read_input_from_string(input_str)
    graph = build_graph(edges)

    result = {'max_dist': 0, 'max_path': []}

    # グラフ内のすべてのノードを探索開始点としてDFS
    nodes = set()
    for u, v, w in edges:
        nodes.add(u)
        nodes.add(v)

    for start in nodes:
        dfs(graph, start, set(), [], 0, result)

    # 結果を \r\n 区切りで標準出力
    output_str = "\r\n".join(str(node) for node in result['max_path'])
    sys.stdout.write(output_str)
    sys.stdout.write("\r\n")  # 最後に改行
