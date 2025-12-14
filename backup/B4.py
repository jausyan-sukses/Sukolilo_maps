import tkinter as tk
from PIL import Image, ImageTk
import os
import numpy as np
import json
import heapq

CANVAS_WIDTH = 1600
CANVAS_HEIGHT = 800
NODE_RADIUS = 6
HIT_RADIUS = 12
MAP_PATH = "map4.png"
SAVE_FILE = "data4.json"
OFFSET_CLOSE_DIST = 100

class Node:
    def __init__(self, index, canvas_id, x, y):
        self.index = index
        self.canvas_id = canvas_id
        self.x = x
        self.y = y
    
    def __repr__(self):
        return 

class MapApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SIGMA MAP E SUROBOYO")
        self.geometry(f"{CANVAS_WIDTH}x{CANVAS_HEIGHT + 50}")

        self.nodes = []
        self.lines = []
        self.node_index_counter = 0

        self.mode = None
        self.curr_node = None
        self.turn_curr_nodes = []
        self.find_quick_selected = []

        self.canvas = tk.Canvas(self, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="black")
        self.canvas.pack()
        self.load_latar()
        
        self.buat_button()

        self.load_nodes()
        self.canvas.bind("<Button-1>", self.cek_klik_canvas)
        self.protocol("WM_DELETE_WINDOW", self.pas_closing)
    
    def load_latar(self):
        backg_gambar = Image.open(MAP_PATH).resize((CANVAS_WIDTH, CANVAS_HEIGHT))
        self.bg_photo = ImageTk.PhotoImage(backg_gambar)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_photo)
    
    def buat_button(self):
        frame = tk.Frame(self)
        frame.pack(side="top", fill="x", pady=5) 
        buttons = [
            ("Draw Node", self.set_draw_mode),
            ("Delete", self.set_delete_mode),
            ("Connect Nodes", self.set_connect_mode),
            ("Create Turn", self.set_turn_mode),
            ("Print List", self.print_jalur2),
            ("Find Quick", self.set_find_quick_mode)
        ]
        for text, command in buttons:
            tk.Button(frame, text=text, command=command).pack(side="left")

    def set_draw_mode(self):
        self.mode = "draw"
        print("Mode Draw, Draw node bebas")

    def set_delete_mode(self):
        self.mode = "delete"
        print("Dell mode")

    def set_connect_mode(self):
        self.mode = "connect"
        self.curr_node = None
        print("COnnect modee")

    def set_turn_mode(self):
        self.mode = "turn"
        self.turn_curr_nodes = []
        print("turn mode")
    
    def set_find_quick_mode(self):
        self.mode = "find_quick"
        self.find_quick_selected = []
        print("Golek mode")

    def cek_klik(self, x, y):
        for node in self.nodes:
            if (x - node.x) ** 2 + (y - node.y) ** 2 <= HIT_RADIUS ** 2:
                return node
        return None
    
    def cek_pose_node(self, x, y):
        return min(self.nodes, key=lambda n: (n.x - x)**2 + (n.y - y)**2)
    
    def hitung_euclidean(self, x1, y1, x2, y2):
        return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    def draw_node_dicanvas(self, node):
        node.canvas_id = self.canvas.create_oval(node.x - NODE_RADIUS, node.y - NODE_RADIUS, node.x + NODE_RADIUS, node.y + NODE_RADIUS, fill="red", width=2)
        self.canvas.create_text(node.x, node.y - 15, text=str(node.index), fill="red", font=("Arial", 10))
    
    def draw_line_dicanvas(self, line_data):
        if line_data['type'] == 'straight':
            return self.canvas.create_line(line_data['points'], fill="blue", width=2)
        elif line_data['type'] == 'curve':
            return self.canvas.create_line(line_data['points'], fill="blue", width=3, smooth=True)
        return None
    
    def save_nodes(self):
        data = {
            "node_index_counter": self.node_index_counter,
            "nodes": [{"index": n.index, "x": n.x, "y": n.y} for n in self.nodes],
            "lines": [{"type": l["type"], "points": l["points"]} for l in self.lines]
        }
        with open(SAVE_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"saveeee aman {len(self.nodes)} nodes and {len(self.lines)} lines")
    
    def load_nodes(self):
        if not os.path.exists(SAVE_FILE):
            return
        
        with open(SAVE_FILE, 'r') as f:
            data = json.load(f)
        
        self.node_index_counter = data.get("node_index_counter", 0)
        self.nodes.clear()
        self.lines.clear()

        for node_data in data["nodes"]:
            x, y, index = node_data["x"], node_data["y"], node_data["index"]
            canvas_id = self.canvas.create_oval(x - NODE_RADIUS, y - NODE_RADIUS, x + NODE_RADIUS, y + NODE_RADIUS, fill="red", width=2)
            self.canvas.create_text(x, y - 15, text=str(index), fill="red", font=("Arial", 10))
            self.nodes.append(Node(index, canvas_id, x, y))

        for line_data in data.get("lines", []):
            line_id = self.draw_line_dicanvas(line_data)
            if line_id:
                self.lines.append({
                    'type': line_data['type'],
                    'points': line_data['points'],
                    'canvas_id': line_id
                })
        
        print(f"yeay loaded {len(self.nodes)} nodes and {len(self.lines)} lines")
        
    def pas_closing(self):
        self.save_nodes()
        self.destroy()

    def add_node(self, x, y):
        canvas_id = self.canvas.create_oval(x - NODE_RADIUS, y - NODE_RADIUS, x + NODE_RADIUS, y + NODE_RADIUS, fill="red", width=2)
        self.canvas.create_text(x, y - 15, text=str(self.node_index_counter), fill="red", font=("Arial", 10))
        new_node = Node(self.node_index_counter, canvas_id, x, y)
        self.nodes.append(new_node)
        print(f"Added node {self.node_index_counter} at ({x}, {y})")
        self.node_index_counter += 1
        self.save_nodes()
        return new_node
    
    def print_jalur2(self):
        for line in self.lines:
            if line['type'] == 'straight' and len(line['points']) == 4:
                x1, y1, x2, y2 = line['points']
                n1 = self.cek_pose_node(x1, y1)
                n2 = self.cek_pose_node(x2, y2)
                print(f"{n1.index} --> {n2.index} (straight lurus)")
            elif line['type'] == 'curve' and len(line['points']) >= 4:
                x1, y1 = line['points'][0], line['points'][1]
                x2, y2 = line['points'][-2], line['points'][-1]
                n1 = self.cek_pose_node(x1, y1)
                n2 = self.cek_pose_node(x2, y2)
                print(f"{n1.index} --> {n2.index} (curve belok)")

    def cek_klik_canvas(self, event):
        x = event.x 
        y = event.y

        if self.mode == "draw":
            self.add_node(x, y)
        
        elif self.mode == "delete":
            node = self.cek_klik(x, y)
            if node:
                self.canvas.delete(node.canvas_id)
                self.nodes.remove(node)
                print(f"delling {node.index}")
                self.save_nodes()
        
        elif self.mode == "connect":
            node = self.cek_klik(x, y)
            if node:
                if self.curr_node is None:
                    self.curr_node = node
                    print(f"curr node {node.index}")
                else:
                    line_id = self.canvas.create_line(self.curr_node.x, self.curr_node.y, node.x, node.y, fill="blue", width=2)
                    self.lines.append({
                        'type': 'straight',
                        'points': [self.curr_node.x, self.curr_node.y, 
                                  node.x, node.y],
                        'canvas_id': line_id
                    })
                    self.save_nodes()
                    self.curr_node = None
        
        elif self.mode == "turn":
            node = self.cek_klik(x, y)
            if node:
                self.turn_curr_nodes.append(node)
                print(f"curr node {node.index} for turn")
                
                if len(self.turn_curr_nodes) == 2:
                    self.make_belokan()
        
        elif self.mode == "find_quick":
            node = self.cek_klik(x, y)
            if node:
                self.find_quick_selected.append(node)
                print(f"curr nodee {node.index}")
                
                if len(self.find_quick_selected) == 2:
                    self.golek_algorithm_mode()
    
    def make_belokan(self):
        start_node, end_node = self.turn_curr_nodes
        print(f"turning {start_node.index} to {end_node.index}")
        
        path = self.cek_close_jalur(start_node, end_node)
        
        if len(path) >= 2:
            points = [coord for node in path for coord in (node.x, node.y)]
            
            nodes_to_delete = path[1:-1]
            for node in nodes_to_delete:
                if node in self.nodes:
                    self.nodes.remove(node)
                    print(f"apus node helper {node.index}")

            self.redraw_all()
            curve_id = self.canvas.create_line(points, fill="blue", width=2, smooth=True)
            self.lines.append({
                'type': 'curve',
                'points': points,
                'canvas_id': curve_id
            })
            self.save_nodes()
            print(f"belok berhasil yeay!!! Delll {len(nodes_to_delete)} helper node")
        else:
            pass
                
        self.turn_curr_nodes = []
        self.mode = None
    
    def golek_algorithm_mode(self):
        start_node, end_node = self.find_quick_selected
        print(f"dari {start_node.index} ke {end_node.index}")
        
        path, total_dist = self.dijkstra_shortest_path(start_node, end_node)
        
        if path:
            path_str = " --> ".join(str(n.index) for n in path)
            print(f"paling cepat lewat: {path_str}")
            print(f"total dist: {total_dist:.2f} units\n")
        else:
            print("gaada jalan cak\n")
        
        self.find_quick_selected = []
        self.mode = None
    
    def cek_close_jalur(self, start_node, end_node):
        path = [start_node]
        wis_visited = {start_node.index}
        currrrr = start_node
        
        for _ in range(len(self.nodes)):
            if currrrr == end_node:
                break

            hampir = [
                (self.hitung_euclidean(node.x, node.y, currrrr.x, currrrr.y), node)
                for node in self.nodes
                if node.index not in wis_visited 
                and self.hitung_euclidean(node.x, node.y, currrrr.x, currrrr.y) <= OFFSET_CLOSE_DIST
            ]
            
            if not hampir:
                if self.hitung_euclidean(end_node.x, end_node.y, currrrr.x, currrrr.y) <= OFFSET_CLOSE_DIST * 1.5:
                    path.append(end_node)
                break

            hampir.sort(key=lambda x: x[0])
            currrrr_dist_to_end = self.hitung_euclidean(end_node.x, end_node.y, currrrr.x, currrrr.y)
            
            best_node = None
            for _, node in hampir:
                node_dist_to_end = self.hitung_euclidean(end_node.x, end_node.y, node.x, node.y)
                if node == end_node or node_dist_to_end < currrrr_dist_to_end:
                    best_node = node
                    break
            
            if best_node is None:
                best_node = hampir[0][1]
            
            path.append(best_node)
            wis_visited.add(best_node.index)
            currrrr = best_node
        
        return path
    
    def dijkstra_shortest_path(self, start_node, end_node):

        graff = {node.index: [] for node in self.nodes}
        
        for line in self.lines:
            if line['type'] == 'straight' and len(line['points']) == 4:
                x1, y1, x2, y2 = line['points']
                n1 = self.cek_pose_node(x1, y1)
                n2 = self.cek_pose_node(x2, y2)
                dist = self.hitung_euclidean(n1.x, n1.y, n2.x, n2.y)
                graff[n1.index].append((n2.index, dist))
                graff[n2.index].append((n1.index, dist))
                
            elif line['type'] == 'curve' and len(line['points']) >= 4:
                x1, y1 = line['points'][0], line['points'][1]
                x2, y2 = line['points'][-2], line['points'][-1]
                n1 = self.cek_pose_node(x1, y1)
                n2 = self.cek_pose_node(x2, y2)
                dist = self.hitung_euclidean(n1.x, n1.y, n2.x, n2.y)
                graff[n1.index].append((n2.index, dist))
                graff[n2.index].append((n1.index, dist))

        antri_prior = [(0, start_node.index)]
        dowo = {node.index: float('inf') for node in self.nodes}
        dowo[start_node.index] = 0
        dalan_prev = {node.index: None for node in self.nodes}
        wis_visited = set()
        
        while antri_prior:
            currrrr_dist, currrrr_idx = heapq.heappop(antri_prior)
            
            if currrrr_idx in wis_visited:
                continue
            wis_visited.add(currrrr_idx)
            
            if currrrr_idx == end_node.index:
                break
            
            for index_tonggo, edge_dist in graff[currrrr_idx]:
                if index_tonggo not in wis_visited:
                    new_dist = currrrr_dist + edge_dist
                    if new_dist < dowo[index_tonggo]:
                        dowo[index_tonggo] = new_dist
                        dalan_prev[index_tonggo] = currrrr_idx
                        heapq.heappush(antri_prior, (new_dist, index_tonggo))

        if dowo[end_node.index] == float('inf'):
            return None, float('inf')
        
        path = []
        currrrr = end_node.index
        while currrrr is not None:
            node = next(n for n in self.nodes if n.index == currrrr)
            path.append(node)
            currrrr = dalan_prev[currrrr]
        
        path.reverse()
        return path, dowo[end_node.index]
    
    def redraw_all(self):
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_photo)
        
        for line_data in self.lines:
            line_data['canvas_id'] = self.draw_line_dicanvas(line_data)

        for node in self.nodes:
            self.draw_node_dicanvas(node)
        
    def setupp(self):
        self.canvas.bind("<Button-1>", self.clickingg)

if __name__ == "__main__":
    app = MapApp()
    app.mainloop()