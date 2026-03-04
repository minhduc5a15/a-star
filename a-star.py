import os
import heapq


class AStarAlgorithm:
    def __init__(self):
        self.graph = {}
        self.heuristics = {}
        self.start_node = None
        self.end_node = None

    def load_data(self, filepath="input.txt"):
        with open(filepath, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
            self.start_node = lines[0].split()[-1]
            self.end_node = lines[1].split()[-1]
            for line in lines[2:]:
                parts = line.split()
                if len(parts) == 2:
                    self.heuristics[parts[0]] = int(parts[1])
                elif len(parts) == 3:
                    u, v, cost = parts[0], parts[1], int(parts[2])
                    if u not in self.graph:
                        self.graph[u] = []
                    self.graph[u].append((v, cost))

    def solve(self):
        start_f = self.heuristics.get(self.start_node, 0)

        L = [(start_f, 0, self.start_node)]
        heapq.heapify(L)

        best_g = {self.start_node: 0}
        parent = {}

        closed_set = set()

        steps_log = []

        while L:
            current_f, current_g, u = heapq.heappop(L)

            if u in closed_set:
                continue
            closed_set.add(u)

            if u == self.end_node:
                sorted_L = sorted(L, key=lambda x: x[0])
                steps_log.append({"u": u, "neighbors": [], "L_snapshot": sorted_L})

                path = []
                while u in parent:
                    path.append(u)
                    u = parent[u]
                path.append(self.start_node)
                path.reverse()
                return steps_log, path, current_g

            neighbors_info = []

            for v, k in self.graph.get(u, []):
                h_v = self.heuristics.get(v, 0)
                g_v = current_g + k
                f_v = g_v + h_v

                if v not in best_g or g_v < best_g[v]:
                    best_g[v] = g_v
                    parent[v] = u
                    heapq.heappush(L, (f_v, g_v, v))

                    neighbors_info.append(
                        {"v": v, "k": k, "h": h_v, "g": g_v, "f": f_v}
                    )

            sorted_L = sorted(L, key=lambda x: x[0])

            steps_log.append(
                {"u": u, "neighbors": neighbors_info, "L_snapshot": sorted_L}
            )

        return steps_log, None, -1

    def write_output(self, filepath, steps_log, path, cost):
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("BẢNG CÁC BƯỚC THỰC HIỆN THUẬT TOÁN A*\n")
            f.write("-" * 90 + "\n")
            f.write(
                f"{'TT':<4} | {'TTK':<4} | {'k(u,v)':<8} | {'h(v)':<6} | {'g(v)':<6} | {'f(v)':<6} | {'Danh sách L':<30}\n"
            )
            f.write("-" * 90 + "\n")

            for step in steps_log:
                u = step["u"]
                neighbors = step["neighbors"]
                L_str = ", ".join(
                    [f"{node}{f_val}" for f_val, _, node in step["L_snapshot"]]
                )

                if not neighbors:
                    f.write(
                        f"{u:<4} | {'-':<4} | {'-':<8} | {'-':<6} | {'-':<6} | {'-':<6} | [{L_str}]\n"
                    )
                    f.write("-" * 90 + "\n")
                    continue

                for i, nb in enumerate(neighbors):
                    ttk, k_val, h_val, g_val, f_val = (
                        nb["v"],
                        nb["k"],
                        nb["h"],
                        nb["g"],
                        nb["f"],
                    )
                    if i == 0:
                        f.write(
                            f"{u:<4} | {ttk:<4} | {k_val:<8} | {h_val:<6} | {g_val:<6} | {f_val:<6} | [{L_str}]\n"
                        )
                    else:
                        f.write(
                            f"{'':<4} | {ttk:<4} | {k_val:<8} | {h_val:<6} | {g_val:<6} | {f_val:<6} | \n"
                        )

                f.write("-" * 90 + "\n")

            f.write("\n")
            if path:
                f.write(f"=> TTKT/dừng, đường đi {' <- '.join(reversed(path))}\n")
                f.write(f"Độ dài: {cost}\n")
            else:
                f.write("Không tìm thấy đường đi!\n")


if __name__ == "__main__":
    astar = AStarAlgorithm()
    input_file = "input.txt"
    output_file = "output.txt"

    if os.path.exists(input_file):
        astar.load_data(input_file)
        logs, final_path, total_cost = astar.solve()
        astar.write_output(output_file, logs, final_path, total_cost)
        print(f"Thành công! Hãy mở file {output_file} để xem kết quả.")
    else:
        print(f"Lỗi: Không tìm thấy file {input_file}")
