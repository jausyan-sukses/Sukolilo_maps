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
SAVE_FILE = "data3.json"
CLOSE_DISTANCE_THRESHOLD = 100  

class Node:
    def __init__(self, index, canvas_id, x, y):
        self.index = index 
        self.canvas_id = canvas_id 
        self.x = x  
        self.y = y  
        self.next = None  
    
    def __repr__(self):
        next_index = self.next.index if self.next else None
        return f"curr node({self.index}, next nodee = {next_index})"

class MapAppppss(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SIGMA MAPSSS - Linked List")
        self.geometry(f"{CANVAS_WIDTH}x{CANVAS_HEIGHT + 50}")
        self.nodes = []  
        self.lines = []
        self.node_index_counter = 0 
        self.mode = None
        self.selected_node = None
        self.canvas = tk.Canvas(self, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="black")
        self.canvas.pack()
        frame = tk.Frame(self)
        frame.pack(side="bottom", fill="x")
        self.draw_node_btn = tk.Button(frame, text="Draw Node", command=self.drawwing_modee)
        self.draw_node_btn.pack(side="left")
        self.delete_node_btn = tk.Button(frame, text="Delete", command=self.dell_nodesss)
        self.delete_node_btn.pack(side="left")
        self.connect_node_btn = tk.Button(frame, text="Connect Nodes", command=self.connect_modee)
        self.connect_node_btn.pack(side="left")
        self.turn_btn = tk.Button(frame, text="Create Turn", command=self.turn_modee)
        self.turn_btn.pack(side="left")
        self.print_list_btn = tk.Button(frame, text="Print List", command=self.print_linked_list)
        self.print_list_btn.pack(side="left")

        latar = Image.open(MAP_PATH)
        latar = latar.resize((CANVAS_WIDTH, CANVAS_HEIGHT))
        self.latar = ImageTk.PhotoImage(latar)
        self.canvas_latar = self.canvas.create_image(0, 0, anchor="nw", image=self.latar)

        self.drawing_mode = False
        self.deleting_mode = False
        self.turn_mode = False
        self.turn_selected_nodes = []
        self.load_nodes()  
        self.setupp()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  
    
    def is_close_nodes(self, x1, y1, x2, y2):
        distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return distance <= CLOSE_DISTANCE_THRESHOLD
    
    def connect_modee(self):
        self.mode = "connect"
        self.drawing_mode = False
        print("connect mode - choose curr node and goals")

    def dell_nodesss(self):
        self.mode = "delete"
        self.deleting_mode = True
        self.drawing_mode = False

    def drawwing_modee(self):
        self.drawing_mode = True
        self.mode = None
        self.turn_mode = False
    
    def turn_modee(self):
        self.mode = "turn"
        self.turn_mode = True
        self.drawing_mode = False
        self.turn_selected_nodes = []
        print("Turn mode: Select start node and end node of the curve")
    
    def save_nodes(self):
        data = {
            "node_index_counter": self.node_index_counter,
            "nodes": [],
            "lines": []
        }
        
        for node in self.nodes:
            node_data = {
                "index": node.index,
                "x": node.x,
                "y": node.y,
                "next_index": node.next.index if node.next else None
            }
            data["nodes"].append(node_data)
        
        # Save all lines (both straight and curved)
        for line_data in self.lines:
            data["lines"].append({
                "type": line_data["type"],
                "points": line_data["points"]
            })
        
        with open(SAVE_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"{SAVE_FILE} - Saved {len(self.nodes)} nodes and {len(self.lines)} lines")
    
    def load_nodes(self):
        if not os.path.exists(SAVE_FILE):
            return
        
        with open(SAVE_FILE, 'r') as f:
            data = json.load(f)
            
        self.node_index_counter = data.get("node_index_counter", 0)
        node_map = {}  

        for node_data in data["nodes"]:
            x = node_data["x"]
            y = node_data["y"]
            index = node_data["index"]
            canvas_id = self.canvas.create_oval(x - NODE_RADIUS, y - NODE_RADIUS, x + NODE_RADIUS, y + NODE_RADIUS, fill="red", width=2)
            self.canvas.create_text(x, y - 15, text=str(index), fill="red", font=("Arial", 10))
            new_node = Node(index, canvas_id, x, y)
            self.nodes.append(new_node)
            node_map[index] = new_node

        for node_data in data["nodes"]:
             if node_data["next_index"] is not None:
                current_node = node_map[node_data["index"]]
                next_node = node_map[node_data["next_index"]]
                current_node.next = next_node
                line_id = self.canvas.create_line(current_node.x, current_node.y, next_node.x, next_node.y, fill="blue", width=2)
                self.lines.append({
                    'type': 'straight',
                    'points': [current_node.x, current_node.y, next_node.x, next_node.y],
                    'canvas_id': line_id
                })
        
        # Load all saved lines (including curved lines)
        if "lines" in data:
            for line_data in data["lines"]:
                line_type = line_data["type"]
                points = line_data["points"]
                
                if line_type == "straight":
                    line_id = self.canvas.create_line(points, fill="blue", width=2)
                elif line_type == "curve":
                    line_id = self.canvas.create_line(points, fill="blue", width=3, smooth=True)
                
                self.lines.append({
                    'type': line_type,
                    'points': points,
                    'canvas_id': line_id
                })
            
        print(f"{SAVE_FILE}: {len(self.nodes)} nodes, {len(self.lines)} lines")
        
    def on_closing(self):
        self.save_nodes()
        self.destroy()

    def draww_nodesss(self, x, y):
        canvas_id = self.canvas.create_oval(x - NODE_RADIUS, y - NODE_RADIUS, x + NODE_RADIUS, y + NODE_RADIUS, fill="red", width=2)
        new_node = Node(self.node_index_counter, canvas_id, x, y)
        self.nodes.append(new_node)
        self.canvas.create_text(x, y - 15, text=str(self.node_index_counter), fill="red", font=("Arial", 10))
        print(f"{self.node_index_counter} ({x}, {y})")
        self.node_index_counter += 1
        self.save_nodes() 
        return new_node
    
    def print_linked_list(self):
        if not self.nodes:
            return
        
        for node in self.nodes:
            print(f"Node {node.index} {node.next.index}")

    def clickingg(self, event):
        if self.drawing_mode == True:
            x = event.x
            y = event.y
            self.draww_nodesss(x, y)
            
        elif self.mode == "delete":
            for node in self.nodes:
                if (event.x - node.x) ** 2 + (event.y - node.y) ** 2 <= HIT_RADIUS ** 2:
                    self.canvas.delete(node.canvas_id)
                    for other_node in self.nodes:
                        if other_node.next == node:
                            other_node.next = None

                    self.nodes.remove(node)
                    print(f"dell {node.index}")
                    self.save_nodes()  
                    break
                    
        elif self.mode == "connect":
            clicked_node = None
            for node in self.nodes:
                if (event.x - node.x) ** 2 + (event.y - node.y) ** 2 <= HIT_RADIUS ** 2:
                    clicked_node = node
                    break
            
            if clicked_node:
                if self.selected_node is None:
                    self.selected_node = clicked_node
                    print(f"curr nodee {clicked_node.index}")
                else:
                    self.selected_node.next = clicked_node
                    line_id = self.canvas.create_line(self.selected_node.x, self.selected_node.y, clicked_node.x, clicked_node.y, fill="blue", width=2)
                    print(f"Garis LURUS: {self.selected_node.index} -> {clicked_node.index}")
                    
                    self.lines.append({
                        'type': 'straight',
                        'points': [self.selected_node.x, self.selected_node.y, clicked_node.x, clicked_node.y],
                        'canvas_id': line_id
                    })
                    length = np.sqrt(
                        (clicked_node.x - self.selected_node.x) ** 2 + 
                        (clicked_node.y - self.selected_node.y) ** 2
                    )
                    
                    print(f"{self.selected_node.index} {clicked_node.index}")
                    print(f"lenghtt = {length:.2f}")
                    
                    self.save_nodes()  
                    self.selected_node = None
        
        elif self.turn_mode and self.mode == "turn":
            # Find clicked node
            clicked_node = None
            for node in self.nodes:
                if (event.x - node.x) ** 2 + (event.y - node.y) ** 2 <= HIT_RADIUS ** 2:
                    clicked_node = node
                    break
            
            if clicked_node:
                self.turn_selected_nodes.append(clicked_node)
                print(f"Turn: Selected node {clicked_node.index}")
                
                # When 2 nodes selected, create the curve
                if len(self.turn_selected_nodes) == 2:
                    start_node = self.turn_selected_nodes[0]
                    end_node = self.turn_selected_nodes[1]
                    
                    print(f"Creating turn from node {start_node.index} to {end_node.index}")
                    
                    # Find all nodes in path from start to end by following adjacent nodes
                    path = self.find_adjacent_path(start_node, end_node)
                    
                    if len(path) >= 2:
                        # Store curve points
                        points = []
                        for node in path:
                            points.append(node.x)
                            points.append(node.y)
                        
                        print(f"Creating curve through {len(path)} nodes")
                        
                        # Delete intermediate nodes (keep start and end)
                        nodes_to_delete = path[1:-1]
                        for node in nodes_to_delete:
                            # Remove from nodes list
                            if node in self.nodes:
                                self.nodes.remove(node)
                            print(f"Deleted intermediate node {node.index}")
                        
                        # Redraw everything including the new curve
                        self.redraw_all()
                        
                        # Now draw smooth curve on top
                        curve_line = self.canvas.create_line(points, fill="blue", width=3, smooth=True)
                        self.lines.append({
                            'type': 'curve',
                            'points': points,
                            'canvas_id': curve_line
                        })
                        
                        self.save_nodes()
                        print(f"Turn created! Deleted {len(nodes_to_delete)} intermediate nodes")
                    else:
                        print("Not enough adjacent nodes found between start and end")
                    
                    # Reset turn mode
                    self.turn_selected_nodes = []
                    self.turn_mode = False
                    self.mode = None
        
    def find_adjacent_path(self, start_node, end_node):
        """Find path of adjacent nodes from start to end using BFS-like approach"""
        path = [start_node]
        visited = set([start_node.index])
        current = start_node
        
        # Try to build path by always choosing closest unvisited node
        max_iterations = len(self.nodes)
        for _ in range(max_iterations):
            if current == end_node:
                break
            
            # Find all unvisited nodes close to current
            candidates = []
            for node in self.nodes:
                if node.index not in visited:
                    dist = np.sqrt((node.x - current.x)**2 + (node.y - current.y)**2)
                    if dist <= CLOSE_DISTANCE_THRESHOLD:
                        candidates.append((dist, node))
            
            if not candidates:
                # No more adjacent nodes, try to jump to end if close
                dist_to_end = np.sqrt((end_node.x - current.x)**2 + (end_node.y - current.y)**2)
                if dist_to_end <= CLOSE_DISTANCE_THRESHOLD * 1.5:
                    path.append(end_node)
                break
            
            # Choose the node that is closest to current AND gets us closer to end
            candidates.sort(key=lambda x: x[0])
            
            # Prioritize nodes that move us toward the end
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
            
            # If no node gets us closer, just take the closest
            if best_node is None:
                best_node = candidates[0][1]
            
            path.append(best_node)
            visited.add(best_node.index)
            current = best_node
        
        return path
    
    def redraw_all(self):
        """Redraw all nodes and their labels"""
        # Clear and redraw background
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.latar)
        
        # Redraw all lines first (so they appear behind nodes)
        for line_data in self.lines:
            if line_data['type'] == 'straight':
                line_id = self.canvas.create_line(line_data['points'], fill="blue", width=2)
            elif line_data['type'] == 'curve':
                line_id = self.canvas.create_line(line_data['points'], fill="blue", width=3, smooth=True)
            line_data['canvas_id'] = line_id
        
        # Redraw all nodes on top
        for node in self.nodes:
            node.canvas_id = self.canvas.create_oval(
                node.x - NODE_RADIUS, node.y - NODE_RADIUS,
                node.x + NODE_RADIUS, node.y + NODE_RADIUS,
                fill="red", width=2
            )
            self.canvas.create_text(node.x, node.y - 15, text=str(node.index),
                                   fill="red", font=("Arial", 10))
        
    def setupp(self):
        self.canvas.bind("<Button-1>", self.clickingg)

if __name__ == "__main__":
    app = MapAppppss()
    app.mainloop()  