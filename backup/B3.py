import tkinter as tk
from PIL import Image, ImageTk
import os
import numpy as np
import json

CANVAS_WIDTH = 1600
CANVAS_HEIGHT = 800
SIDEBAR_WIDTH = 200
NODE_RADIUS = 6
HIT_RADIUS = 12
MAP_PATH = "map4.png"
SAVE_FILE = "data4.json"
CLOSE_DISTANCE_THRESHOLD = 100  

class Node:
    def __init__(self, index, canvas_id, x, y):
        self.index = index
        self.canvas_id = canvas_id
        self.x = x
        self.y = y
    def __repr__(self):
        return f"Node({self.index})"

class MapApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SIGMA MAP SUROBOYO")
        self.geometry(f"{CANVAS_WIDTH}x{CANVAS_HEIGHT + 50}")
        self.nodes = []
        self.lines = []
        self.node_index_counter = 0
        self.mode = None
        self.selected_node = None
        self.drawing_mode = False
        self.turn_mode = False
        self.turn_selected_nodes = []

        self.canvas = tk.Canvas(self, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="black")
        self.canvas.pack()
        frame = tk.Frame(self)
        frame.pack(side="bottom", fill="x")
        tk.Button(frame, text="Draw Node", command=self.set_draw_mode).pack(side="left")
        tk.Button(frame, text="Delete", command=self.set_delete_mode).pack(side="left")
        tk.Button(frame, text="Connect Nodes", command=self.set_connect_mode).pack(side="left")
        tk.Button(frame, text="Create Turn", command=self.set_turn_mode).pack(side="left")
        tk.Button(frame, text="Print List", command=self.print_connections).pack(side="left")

        latar = Image.open(MAP_PATH)
        latar = latar.resize((CANVAS_WIDTH, CANVAS_HEIGHT))
        self.latar = ImageTk.PhotoImage(latar)
        self.canvas.create_image(0, 0, anchor="nw", image=self.latar)

        self.load_nodes()
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def close_kah(self, x1, y1, x2, y2):
        distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return distance <= CLOSE_DISTANCE_THRESHOLD
    
    def set_draw_mode(self):
        self.drawing_mode = True
        self.mode = None
        self.turn_mode = False

    def set_delete_mode(self):
        self.mode = "delete"
        self.drawing_mode = False
        self.turn_mode = False

    def set_connect_mode(self):
        self.mode = "connect"
        self.drawing_mode = False
        self.turn_mode = False
        print("Connect mode: select two nodes to connect.")

    def set_turn_mode(self):
        self.mode = "turn"
        self.drawing_mode = False
        self.turn_mode = True
        self.turn_selected_nodes = []
        print("Turn mode: select start and end nodes.")
    
    def save_nodes(self):
        data = {
            "node_index_counter": self.node_index_counter,
            "nodes": [
                {"index": n.index, "x": n.x, "y": n.y}
                for n in self.nodes
            ],
            "lines": [
                {"type": l["type"], "points": l["points"]}
                for l in self.lines
            ]
        }
        with open(SAVE_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"{SAVE_FILE} - Saved {len(self.nodes)} nodes and {len(self.lines)} lines")
    
    def load_nodes(self):
        if not os.path.exists(SAVE_FILE):
            return
        with open(SAVE_FILE, 'r') as f:
            data = json.load(f)
        self.node_index_counter = data.get("node_index_counter", 0)
        self.nodes.clear()
        self.lines.clear()
        # Draw nodes
        for node_data in data["nodes"]:
            x, y, index = node_data["x"], node_data["y"], node_data["index"]
            canvas_id = self.canvas.create_oval(x - NODE_RADIUS, y - NODE_RADIUS, x + NODE_RADIUS, y + NODE_RADIUS, fill="red", width=2)
            self.canvas.create_text(x, y - 15, text=str(index), fill="red", font=("Arial", 10))
            self.nodes.append(Node(index, canvas_id, x, y))
        # Draw lines
        for line_data in data.get("lines", []):
            line_type = line_data["type"]
            points = line_data["points"]
            if line_type == "straight":
                line_id = self.canvas.create_line(points, fill="blue", width=2)
            elif line_type == "curve":
                line_id = self.canvas.create_line(points, fill="blue", width=3, smooth=True)
            else:
                continue
            self.lines.append({
                'type': line_type,
                'points': points,
                'canvas_id': line_id
            })
        print(f"{SAVE_FILE}: {len(self.nodes)} nodes, {len(self.lines)} lines")
        
    def on_closing(self):
        self.save_nodes()
        self.destroy()

    def add_node(self, x, y):
        canvas_id = self.canvas.create_oval(x - NODE_RADIUS, y - NODE_RADIUS, x + NODE_RADIUS, y + NODE_RADIUS, fill="red", width=2)
        self.canvas.create_text(x, y - 15, text=str(self.node_index_counter), fill="red", font=("Arial", 10))
        new_node = Node(self.node_index_counter, canvas_id, x, y)
        self.nodes.append(new_node)
        print(f"Node {self.node_index_counter} at ({x}, {y})")
        self.node_index_counter += 1
        self.save_nodes()
        return new_node
    
    def print_connections(self):
        if not self.nodes:
            print("No nodes in the list")
            return
        print("==== Node Connections ====")
        for line in self.lines:
            if line['type'] == 'straight' and len(line['points']) == 4:
                x1, y1, x2, y2 = line['points']
                n1 = min(self.nodes, key=lambda n: (n.x-x1)**2 + (n.y-y1)**2)
                n2 = min(self.nodes, key=lambda n: (n.x-x2)**2 + (n.y-y2)**2)
                print(f"Node {n1.index} -> Node {n2.index} (straight)")
            elif line['type'] == 'curve' and len(line['points']) >= 4:
                x1, y1 = line['points'][0], line['points'][1]
                x2, y2 = line['points'][-2], line['points'][-1]
                n1 = min(self.nodes, key=lambda n: (n.x-x1)**2 + (n.y-y1)**2)
                n2 = min(self.nodes, key=lambda n: (n.x-x2)**2 + (n.y-y2)**2)
                print(f"Node {n1.index} -> Node {n2.index} (curve)")
        print("=========================")

    def on_canvas_click(self, event):
        x, y = event.x, event.y
        if self.drawing_mode:
            self.add_node(x, y)
        elif self.mode == "delete":
            for node in self.nodes:
                if (x - node.x) ** 2 + (y - node.y) ** 2 <= HIT_RADIUS ** 2:
                    self.canvas.delete(node.canvas_id)
                    self.nodes.remove(node)
                    print(f"Deleted node {node.index}")
                    self.save_nodes()
                    break
        elif self.mode == "connect":
            clicked_node = next((node for node in self.nodes if (x - node.x) ** 2 + (y - node.y) ** 2 <= HIT_RADIUS ** 2), None)
            if clicked_node:
                if self.selected_node is None:
                    self.selected_node = clicked_node
                    print(f"Selected node {clicked_node.index}")
                else:
                    line_id = self.canvas.create_line(self.selected_node.x, self.selected_node.y, clicked_node.x, clicked_node.y, fill="blue", width=2)
                    self.lines.append({
                        'type': 'straight',
                        'points': [self.selected_node.x, self.selected_node.y, clicked_node.x, clicked_node.y],
                        'canvas_id': line_id
                    })
                    print(f"Connected node {self.selected_node.index} -> {clicked_node.index}")
                    self.save_nodes()
                    self.selected_node = None
        elif self.turn_mode and self.mode == "turn":
            clicked_node = next((node for node in self.nodes if (x - node.x) ** 2 + (y - node.y) ** 2 <= HIT_RADIUS ** 2), None)
            if clicked_node:
                self.turn_selected_nodes.append(clicked_node)
                print(f"Turn: Selected node {clicked_node.index}")
                if len(self.turn_selected_nodes) == 2:
                    start_node, end_node = self.turn_selected_nodes
                    print(f"Creating turn from node {start_node.index} to {end_node.index}")
                    path = self.find_adjacent_path(start_node, end_node)
                    if len(path) >= 2:
                        points = [coord for node in path for coord in (node.x, node.y)]
                        nodes_to_delete = path[1:-1]
                        for node in nodes_to_delete:
                            if node in self.nodes:
                                self.nodes.remove(node)
                            print(f"Deleted intermediate node {node.index}")
                        self.redraw_all()
                        curve_line = self.canvas.create_line(points, fill="blue", width=2, smooth=True)
                        self.lines.append({
                            'type': 'curve',
                            'points': points,
                            'canvas_id': curve_line
                        })
                        self.save_nodes()
                        print(f"Turn created! Deleted {len(nodes_to_delete)} intermediate nodes")
                    else:
                        print("Not enough adjacent nodes found between start and end")
                    self.turn_selected_nodes = []
                    self.turn_mode = False
                    self.mode = None
        
    def find_adjacent_path(self, start_node, end_node):
        path = [start_node]
        visited = set([start_node.index])
        current = start_node
        max_iterations = len(self.nodes)
        for _ in range(max_iterations):
            if current == end_node:
                break

            candidates = []
            for node in self.nodes:
                if node.index not in visited:
                    dist = np.sqrt((node.x - current.x)**2 + (node.y - current.y)**2)
                    if dist <= CLOSE_DISTANCE_THRESHOLD:
                        candidates.append((dist, node))
            
            if not candidates:
                dist_to_end = np.sqrt((end_node.x - current.x)**2 + (end_node.y - current.y)**2)
                if dist_to_end <= CLOSE_DISTANCE_THRESHOLD * 1.5:
                    path.append(end_node)
                break

            candidates.sort(key=lambda x: x[0])

            best_node = None
            current_dist_to_end = np.sqrt((end_node.x - current.x)**2 + (end_node.y - current.y)**2)
            
            for dist, node in candidates:
                node_dist_to_end = np.sqrt((end_node.x - node.x)**2 + (end_node.y - node.y)**2)
                if node == end_node:
                    best_node = node
                    break
                elif node_dist_to_end < current_dist_to_end:
                    best_node = node
                    break

            if best_node is None:
                best_node = candidates[0][1]
            
            path.append(best_node)
            visited.add(best_node.index)
            current = best_node
        
        return path
    
    def redraw_all(self):
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.latar)
        for line_data in self.lines:
            if line_data['type'] == 'straight':
                line_id = self.canvas.create_line(line_data['points'], fill="blue", width=2)
            elif line_data['type'] == 'curve':
                line_id = self.canvas.create_line(line_data['points'], fill="blue", width=3, smooth=True)
            line_data['canvas_id'] = line_id
        for node in self.nodes:
            node.canvas_id = self.canvas.create_oval(
                node.x - NODE_RADIUS, node.y - NODE_RADIUS,
                node.x + NODE_RADIUS, node.y + NODE_RADIUS,
                fill="red", width=2
            )
            self.canvas.create_text(node.x, node.y - 15, text=str(node.index), fill="red", font=("Arial", 10))
        
    def setupp(self):
        self.canvas.bind("<Button-1>", self.clickingg)

if __name__ == "__main__":
    app = MapApp()
    app.mainloop()