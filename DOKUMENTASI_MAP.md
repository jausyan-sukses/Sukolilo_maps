# 📍 DOKUMENTASI APLIKASI MAP SUROBOYO

## Pengantar
Aplikasi ini adalah editor peta interaktif yang memungkinkan pengguna untuk:
- Menambah dan menghapus node (titik)
- Menghubungkan node dengan garis lurus
- Membuat jalur melengkung (curved turn)
- Mencari jalur terpendek menggunakan algoritma Dijkstra
- Menyimpan dan memuat data ke/dari file JSON

---

## 1. 🔍 Algoritma Dijkstra dalam Mencari Jalur Terpendek

### Cara Kerja Dijkstra (Penjelasan Sederhana)

Bayangkan Anda ingin pergi dari rumah ke sekolah, dan ada banyak jalan yang bisa dipilih. Algoritma Dijkstra membantu Anda menemukan jalan terpaling pendek dengan cara:

1. **Mulai dari titik awal** (start node)
2. **Lihat semua tetangga** yang terhubung langsung
3. **Hitung jarak** dari titik awal ke setiap tetangga
4. **Pilih tetangga terdekat** yang belum dikunjungi
5. **Ulangi** proses ini sampai mencapai tujuan
6. **Catat jalur** yang dilalui untuk mendapatkan rute terpendek

### Kode yang Berperan

```python
def dijkstra_shortest_path(self, start_node, end_node):
    """Simple Dijkstra algorithm using Euclidean distance"""
    
    # LANGKAH 1: Bangun graf dari semua garis yang ada
    # Graf adalah struktur data yang menyimpan hubungan antar node
    graph = {node.index: [] for node in self.nodes}
    
    # Iterasi semua garis untuk membangun koneksi
    for line in self.lines:
        if line['type'] == 'straight' and len(line['points']) == 4:
            x1, y1, x2, y2 = line['points']
            n1 = self._find_node_at_point(x1, y1)
            n2 = self._find_node_at_point(x2, y2)
            dist = self._euclidean_distance(n1.x, n1.y, n2.x, n2.y)
            
            # Tambahkan koneksi dua arah (bolak-balik)
            graph[n1.index].append((n2.index, dist))
            graph[n2.index].append((n1.index, dist))
            
        elif line['type'] == 'curve':
            # Untuk garis melengkung, ambil titik awal dan akhir
            x1, y1 = line['points'][0], line['points'][1]
            x2, y2 = line['points'][-2], line['points'][-1]
            n1 = self._find_node_at_point(x1, y1)
            n2 = self._find_node_at_point(x2, y2)
            dist = self._euclidean_distance(n1.x, n1.y, n2.x, n2.y)
            
            graph[n1.index].append((n2.index, dist))
            graph[n2.index].append((n1.index, dist))
    
    # LANGKAH 2: Inisialisasi struktur data Dijkstra
    # pq = priority queue (antrian prioritas) untuk memilih node terdekat
    pq = [(0, start_node.index)]  # (jarak, index_node)
    
    # distances = menyimpan jarak terpendek dari start ke setiap node
    distances = {node.index: float('inf') for node in self.nodes}
    distances[start_node.index] = 0  # Jarak ke diri sendiri = 0
    
    # previous = menyimpan node sebelumnya untuk rekonstruksi jalur
    previous = {node.index: None for node in self.nodes}
    
    # visited = set untuk melacak node yang sudah dikunjungi
    visited = set()
    
    # LANGKAH 3: Proses algoritma Dijkstra
    while pq:
        # Ambil node dengan jarak terpendek dari priority queue
        current_dist, current_idx = heapq.heappop(pq)
        
        # Skip jika sudah dikunjungi
        if current_idx in visited:
            continue
        visited.add(current_idx)
        
        # Jika sudah sampai tujuan, berhenti
        if current_idx == end_node.index:
            break
        
        # Periksa semua tetangga (neighbor) dari node saat ini
        for neighbor_idx, edge_dist in graph[current_idx]:
            if neighbor_idx not in visited:
                # Hitung jarak baru melalui node saat ini
                new_dist = current_dist + edge_dist
                
                # Jika jarak baru lebih pendek, update!
                if new_dist < distances[neighbor_idx]:
                    distances[neighbor_idx] = new_dist
                    previous[neighbor_idx] = current_idx
                    heapq.heappush(pq, (new_dist, neighbor_idx))
    
    # LANGKAH 4: Rekonstruksi jalur dari tujuan ke awal
    if distances[end_node.index] == float('inf'):
        return None, float('inf')  # Tidak ada jalur yang ditemukan
    
    path = []
    current = end_node.index
    while current is not None:
        node = next(n for n in self.nodes if n.index == current)
        path.append(node)
        current = previous[current]  # Mundur ke node sebelumnya
    
    path.reverse()  # Balik urutan agar dari start ke end
    return path, distances[end_node.index]
```

### Penjelasan Detail:

- **Priority Queue (heapq)**: Digunakan untuk selalu memilih node dengan jarak terpendek yang belum dikunjungi
- **Distances Dictionary**: Menyimpan jarak terpendek yang diketahui dari start ke setiap node
- **Previous Dictionary**: Menyimpan "jejak" untuk merekonstruksi jalur lengkap
- **Visited Set**: Menandai node yang sudah diproses agar tidak diproses ulang

### Contoh Penggunaan:
1. Klik tombol **"Find Quick"**
2. Klik node awal (misalnya node 0)
3. Klik node tujuan (misalnya node 5)
4. Algoritma akan menampilkan jalur terpendek di terminal, contoh:
   ```
   Shortest path: 0 → 2 → 4 → 5
   Total distance: 450.32 units
   ```

---

## 2. 💾 Menyimpan Data Nodes pada JSON File

### Cara Kerja Penyimpanan Data

Aplikasi ini menyimpan semua data ke file `data4.json` setiap kali ada perubahan (menambah node, menghapus node, membuat koneksi, dll). Data disimpan dalam format JSON yang mudah dibaca manusia.

### Struktur Data JSON

```json
{
  "node_index_counter": 6,
  "nodes": [
    {"index": 0, "x": 100, "y": 200},
    {"index": 1, "x": 300, "y": 150},
    {"index": 2, "x": 500, "y": 300}
  ],
  "lines": [
    {
      "type": "straight",
      "points": [100, 200, 300, 150]
    },
    {
      "type": "curve",
      "points": [300, 150, 350, 200, 450, 280, 500, 300]
    }
  ]
}
```

### Kode untuk Menyimpan Data

```python
def save_nodes(self):
    """Save nodes and lines to JSON file"""
    
    # LANGKAH 1: Buat dictionary dengan semua data
    data = {
        # Counter untuk index node berikutnya
        "node_index_counter": self.node_index_counter,
        
        # List semua node dengan index, koordinat x, dan koordinat y
        "nodes": [
            {"index": n.index, "x": n.x, "y": n.y} 
            for n in self.nodes
        ],
        
        # List semua garis dengan tipe (straight/curve) dan titik-titiknya
        "lines": [
            {"type": l["type"], "points": l["points"]} 
            for l in self.lines
        ]
    }
    
    # LANGKAH 2: Tulis ke file JSON dengan format yang rapi (indent=2)
    with open(SAVE_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Saved {len(self.nodes)} nodes and {len(self.lines)} lines")
```

### Kode untuk Memuat Data

```python
def load_nodes(self):
    """Load nodes and lines from JSON file"""
    
    # LANGKAH 1: Cek apakah file ada
    if not os.path.exists(SAVE_FILE):
        return  # Jika tidak ada, skip
    
    # LANGKAH 2: Baca file JSON
    with open(SAVE_FILE, 'r') as f:
        data = json.load(f)
    
    # LANGKAH 3: Load counter dan bersihkan list lama
    self.node_index_counter = data.get("node_index_counter", 0)
    self.nodes.clear()
    self.lines.clear()

    # LANGKAH 4: Load semua node
    for node_data in data["nodes"]:
        x, y, index = node_data["x"], node_data["y"], node_data["index"]
        
        # Gambar lingkaran merah untuk node
        canvas_id = self.canvas.create_oval(
            x - NODE_RADIUS, y - NODE_RADIUS, 
            x + NODE_RADIUS, y + NODE_RADIUS, 
            fill="red", width=2
        )
        
        # Gambar label angka di atas node
        self.canvas.create_text(x, y - 15, text=str(index), 
                               fill="red", font=("Arial", 10))
        
        # Buat objek Node dan tambahkan ke list
        self.nodes.append(Node(index, canvas_id, x, y))

    # LANGKAH 5: Load semua garis
    for line_data in data.get("lines", []):
        line_id = self._draw_line_on_canvas(line_data)
        if line_id:
            self.lines.append({
                'type': line_data['type'],
                'points': line_data['points'],
                'canvas_id': line_id
            })
    
    print(f"Loaded {len(self.nodes)} nodes and {len(self.lines)} lines")
```

### Penjelasan Detail:

- **json.dump()**: Menulis data Python (dictionary, list) ke file dalam format JSON
- **json.load()**: Membaca file JSON dan mengubahnya menjadi data Python
- **indent=2**: Membuat JSON lebih rapi dan mudah dibaca dengan indentasi 2 spasi
- **List Comprehension**: `[{"index": n.index, ...} for n in self.nodes]` adalah cara singkat membuat list dari loop
- **Auto-save**: Function `save_nodes()` dipanggil otomatis setiap kali ada perubahan

### Kapan Data Disimpan?
- Saat menambah node baru (`add_node()`)
- Saat menghapus node (`on_canvas_click` mode delete)
- Saat menghubungkan node (`on_canvas_click` mode connect)
- Saat membuat curved turn (`_create_turn()`)
- Saat menutup aplikasi (`on_closing()`)

---

## 3. 🌀 Cara Membuat Curve Turn dengan Node Helper

### Apa itu Curve Turn?

Curve Turn adalah garis melengkung yang menghubungkan dua node dengan melewati node-node perantara (helper nodes). Node perantara ini kemudian dihapus setelah garis melengkung dibuat, sehingga hanya tersisa node awal dan akhir.

### Cara Kerja (Step by Step)

1. **Pengguna mengklik tombol "Create Turn"**
2. **Pilih node awal** (klik node pertama)
3. **Pilih node akhir** (klik node kedua)
4. **Sistem mencari jalur** melalui node-node terdekat yang menghubungkan kedua node
5. **Node perantara dihapus**, hanya menyisakan node awal dan akhir
6. **Garis melengkung digambar** mengikuti koordinat semua node yang dilalui

### Kode yang Berperan

#### Fungsi Utama: `_create_turn()`

```python
def _create_turn(self):
    """Create a curved line between two selected nodes"""
    
    # LANGKAH 1: Ambil node awal dan akhir yang dipilih
    start_node, end_node = self.turn_selected_nodes
    print(f"Creating turn from node {start_node.index} to {end_node.index}")
    
    # LANGKAH 2: Cari jalur melalui node-node yang berdekatan
    path = self._find_adjacent_path(start_node, end_node)
    
    if len(path) >= 2:
        # LANGKAH 3: Ubah list node menjadi list koordinat [x1, y1, x2, y2, ...]
        points = [coord for node in path for coord in (node.x, node.y)]
        
        # LANGKAH 4: Tentukan node mana yang akan dihapus (node perantara)
        nodes_to_delete = path[1:-1]  # Semua kecuali node pertama dan terakhir
        
        # LANGKAH 5: Hapus node perantara dari list dan canvas
        for node in nodes_to_delete:
            if node in self.nodes:
                self.nodes.remove(node)
                print(f"Deleted intermediate node {node.index}")
        
        # LANGKAH 6: Gambar ulang seluruh canvas
        self.redraw_all()
        
        # LANGKAH 7: Gambar garis melengkung dengan smooth=True
        curve_id = self.canvas.create_line(
            points, 
            fill="blue", 
            width=2, 
            smooth=True  # Ini yang membuat garis menjadi melengkung!
        )
        
        # LANGKAH 8: Simpan data garis ke list
        self.lines.append({
            'type': 'curve',
            'points': points,
            'canvas_id': curve_id
        })
        
        # LANGKAH 9: Simpan ke file JSON
        self.save_nodes()
        print(f"Turn created! Deleted {len(nodes_to_delete)} intermediate nodes")
    else:
        print("Not enough adjacent nodes for turn")
    
    # Reset mode dan selection
    self.turn_selected_nodes = []
    self.mode = None
```

#### Fungsi Helper: `_find_adjacent_path()`

```python
def _find_adjacent_path(self, start_node, end_node):
    """Find path through adjacent nodes from start to end"""
    
    # LANGKAH 1: Inisialisasi jalur dengan node awal
    path = [start_node]
    visited = {start_node.index}  # Set untuk melacak node yang sudah dikunjungi
    current = start_node
    
    # LANGKAH 2: Loop maksimal sebanyak jumlah node
    for _ in range(len(self.nodes)):
        # Jika sudah sampai tujuan, berhenti
        if current == end_node:
            break

        # LANGKAH 3: Cari node-node yang dekat (dalam radius threshold)
        candidates = [
            (self._euclidean_distance(node.x, node.y, current.x, current.y), node)
            for node in self.nodes
            if node.index not in visited 
            and self._euclidean_distance(node.x, node.y, current.x, current.y) <= CLOSE_DISTANCE_THRESHOLD
        ]
        
        # Jika tidak ada kandidat terdekat
        if not candidates:
            # Coba langsung ke end node jika cukup dekat
            if self._euclidean_distance(end_node.x, end_node.y, current.x, current.y) <= CLOSE_DISTANCE_THRESHOLD * 1.5:
                path.append(end_node)
            break

        # LANGKAH 4: Urutkan kandidat berdasarkan jarak (terdekat dulu)
        candidates.sort(key=lambda x: x[0])
        current_dist_to_end = self._euclidean_distance(end_node.x, end_node.y, current.x, current.y)
        
        # LANGKAH 5: Pilih node yang mendekatkan kita ke tujuan
        best_node = None
        for _, node in candidates:
            node_dist_to_end = self._euclidean_distance(end_node.x, end_node.y, node.x, node.y)
            # Pilih node jika itu adalah tujuan ATAU lebih dekat ke tujuan
            if node == end_node or node_dist_to_end < current_dist_to_end:
                best_node = node
                break
        
        # Jika tidak ada yang lebih dekat, pilih yang terdekat saja
        if best_node is None:
            best_node = candidates[0][1]
        
        # LANGKAH 6: Tambahkan node ke jalur
        path.append(best_node)
        visited.add(best_node.index)
        current = best_node
    
    return path
```

### Penjelasan Detail:

**1. CLOSE_DISTANCE_THRESHOLD = 100**
   - Konstanta yang menentukan seberapa jauh node dianggap "berdekatan"
   - Node hanya akan dipertimbangkan jika jaraknya ≤ 100 pixel

**2. Greedy Algorithm**
   - `_find_adjacent_path()` menggunakan pendekatan greedy (rakus)
   - Selalu memilih node terdekat yang membawa lebih dekat ke tujuan
   - Tidak menjamin jalur terpendek, tapi cepat dan cukup bagus

**3. smooth=True**
   - Parameter Tkinter yang membuat garis melengkung secara otomatis
   - Menggunakan interpolasi untuk membuat kurva halus antar titik

**4. Path Flattening**
   ```python
   points = [coord for node in path for coord in (node.x, node.y)]
   ```
   - Mengubah list Node menjadi list koordinat datar
   - Contoh: `[Node(0), Node(1)]` → `[100, 200, 300, 150]`

**5. Node Deletion**
   ```python
   nodes_to_delete = path[1:-1]  # Slice notation
   ```
   - `[1:-1]` berarti ambil dari index 1 sampai sebelum terakhir
   - Meninggalkan node pertama (start) dan terakhir (end)

### Contoh Visual:

```
Sebelum Create Turn:
Node 0 --- Node 1 --- Node 2 --- Node 3

Setelah Create Turn:
Node 0 ~~~~~~~~~~~~~~~~~~~~ Node 3
         (Node 1 & 2 dihapus)
```

---

## 4. 📏 Bagaimana Cara Menghitung Jarak Antar Node

### Konsep Dasar: Euclidean Distance

Jarak Euclidean adalah jarak garis lurus antara dua titik, seperti menggunakan penggaris. Rumusnya menggunakan Teorema Pythagoras:

```
Jarak = √[(x₂ - x₁)² + (y₂ - y₁)²]
```

### Visualisasi:

```
     (x₁, y₁)
        •
        |\
        | \  ← Jarak yang dicari (hipotenusa)
        |  \
     Δy |   \
        |    \
        •-----•
      (x₁,y₂) (x₂, y₂)
          Δx
```

- **Δx** = selisih horizontal = `x₂ - x₁`
- **Δy** = selisih vertikal = `y₂ - y₁`
- **Jarak** = √(Δx² + Δy²)

### Kode yang Berperan

```python
def _euclidean_distance(self, x1, y1, x2, y2):
    """Calculate Euclidean distance between two points"""
    
    # Hitung selisih koordinat
    delta_x = x2 - x1
    delta_y = y2 - y1
    
    # Kuadratkan selisih
    delta_x_squared = delta_x ** 2
    delta_y_squared = delta_y ** 2
    
    # Jumlahkan dan akar kuadrat
    distance = np.sqrt(delta_x_squared + delta_y_squared)
    
    return distance
```

Atau dalam bentuk singkat (yang digunakan di kode):

```python
def _euclidean_distance(self, x1, y1, x2, y2):
    """Calculate Euclidean distance between two points"""
    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
```

### Contoh Perhitungan:

Misalkan ada dua node:
- **Node A**: koordinat (100, 200)
- **Node B**: koordinat (400, 500)

**Perhitungan manual:**
```
Δx = 400 - 100 = 300
Δy = 500 - 200 = 300

Jarak = √(300² + 300²)
      = √(90000 + 90000)
      = √180000
      = 424.26 pixel
```

**Dalam kode:**
```python
dist = self._euclidean_distance(100, 200, 400, 500)
# Hasil: 424.26
```

### Di Mana Fungsi Ini Digunakan?

#### 1. **Mendeteksi Klik pada Node**
```python
def _get_clicked_node(self, x, y):
    """Find node at click position"""
    for node in self.nodes:
        # Cek jika jarak klik ke node ≤ HIT_RADIUS (12 pixel)
        if (x - node.x) ** 2 + (y - node.y) ** 2 <= HIT_RADIUS ** 2:
            return node
    return None
```
- Menghitung jarak dari posisi klik ke setiap node
- Jika jarak ≤ 12 pixel, dianggap mengklik node tersebut

#### 2. **Mencari Node Terdekat**
```python
def _find_node_at_point(self, x, y):
    """Find closest node to given coordinates"""
    return min(self.nodes, key=lambda n: (n.x - x)**2 + (n.y - y)**2)
```
- Mencari node dengan jarak terkecil ke titik tertentu
- Digunakan saat memuat garis dari JSON untuk mencari node di ujung garis

#### 3. **Menghitung Bobot Edge di Dijkstra**
```python
# Di dalam dijkstra_shortest_path()
dist = self._euclidean_distance(n1.x, n1.y, n2.x, n2.y)
graph[n1.index].append((n2.index, dist))
```
- Menghitung "biaya" atau "berat" dari edge antar node
- Dijkstra menggunakan nilai ini untuk menentukan jalur terpendek

#### 4. **Mencari Node Berdekatan untuk Curve**
```python
# Di dalam _find_adjacent_path()
candidates = [
    (self._euclidean_distance(node.x, node.y, current.x, current.y), node)
    for node in self.nodes
    if ... and self._euclidean_distance(...) <= CLOSE_DISTANCE_THRESHOLD
]
```
- Mencari node yang jaraknya ≤ 100 pixel (CLOSE_DISTANCE_THRESHOLD)
- Hanya node dalam radius ini yang dipertimbangkan untuk jalur melengkung

### Kenapa Pakai NumPy?

```python
import numpy as np

# Menggunakan np.sqrt() bukan math.sqrt()
distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
```

**Keuntungan NumPy:**
- Lebih cepat untuk operasi matematika
- Bisa menghitung banyak jarak sekaligus (vectorization)
- Sudah termasuk banyak fungsi matematika lainnya

### Alternatif Perhitungan Jarak

Selain Euclidean, ada metode lain:

**1. Manhattan Distance (Jarak Taksi)**
```python
distance = abs(x2 - x1) + abs(y2 - y1)
```
- Seperti berjalan di kota dengan blok persegi
- Hanya bisa jalan horizontal atau vertikal

**2. Chebyshev Distance (Jarak Raja Catur)**
```python
distance = max(abs(x2 - x1), abs(y2 - y1))
```
- Jarak maksimum dari dua sumbu
- Seperti pergerakan raja dalam catur

---

## 📝 Ringkasan Alur Kerja Aplikasi

### 1. **Startup**
```
Buka aplikasi → Load JSON → Gambar background → Gambar nodes & lines
```

### 2. **Menambah Node**
```
Klik "Draw Node" → Klik canvas → Node ditambah → Simpan ke JSON
```

### 3. **Menghubungkan Node**
```
Klik "Connect Nodes" → Klik node 1 → Klik node 2 → Garis digambar → Simpan
```

### 4. **Membuat Curve Turn**
```
Klik "Create Turn" → Klik node awal → Klik node akhir 
→ Cari jalur melalui node terdekat → Hapus node perantara 
→ Gambar garis melengkung → Simpan
```

### 5. **Mencari Jalur Terpendek**
```
Klik "Find Quick" → Klik node awal → Klik node tujuan
→ Jalankan Dijkstra → Tampilkan jalur di terminal
```

### 6. **Closing**
```
Tutup aplikasi → Auto-save ke JSON → Selesai
```

---

## 🎯 Fitur-Fitur Utama

| Fitur | Tombol | Fungsi |
|-------|--------|--------|
| Tambah Node | Draw Node | Menambahkan titik baru di peta |
| Hapus Node | Delete | Menghapus node yang diklik |
| Hubungkan Node | Connect Nodes | Membuat garis lurus antar 2 node |
| Buat Belokan | Create Turn | Membuat garis melengkung melalui node helper |
| Lihat Koneksi | Print List | Tampilkan semua koneksi di terminal |
| Cari Jalur | Find Quick | Mencari jalur terpendek dengan Dijkstra |

---

## 🔧 Konfigurasi (Constants)

```python
CANVAS_WIDTH = 1600          # Lebar canvas dalam pixel
CANVAS_HEIGHT = 800          # Tinggi canvas dalam pixel
NODE_RADIUS = 6              # Jari-jari lingkaran node
HIT_RADIUS = 12              # Radius deteksi klik node
MAP_PATH = "map4.png"        # File gambar background
SAVE_FILE = "data4.json"     # File penyimpanan data
CLOSE_DISTANCE_THRESHOLD = 100  # Jarak maksimal untuk node "berdekatan"
```

---

## 📚 Library yang Digunakan

- **tkinter**: GUI framework untuk membuat window dan canvas
- **PIL (Pillow)**: Untuk memuat dan menampilkan gambar background
- **numpy**: Untuk perhitungan matematika (sqrt, dsb)
- **json**: Untuk menyimpan/memuat data ke/dari file
- **heapq**: Untuk priority queue di algoritma Dijkstra
- **os**: Untuk cek keberadaan file

---

## 💡 Tips Penggunaan

1. **Buat Node Terlebih Dahulu** sebelum menghubungkannya
2. **Simpan Regular** - aplikasi auto-save saat perubahan, tapi pastikan tidak crash
3. **Node Helper** untuk curve harus ditempatkan berdekatan (≤ 100 pixel)
4. **Dijkstra** memerlukan koneksi garis antar node untuk bekerja
5. **JSON File** bisa diedit manual jika perlu koreksi data

---

## 🐛 Troubleshooting

**Q: Dijkstra tidak menemukan jalur?**
- Pastikan kedua node terhubung dengan garis (langsung atau tidak langsung)
- Cek apakah ada koneksi yang terputus

**Q: Curve tidak terbentuk?**
- Pastikan ada node perantara dalam radius 100 pixel
- Node perantara harus membentuk jalur yang menghubungkan start dan end

**Q: Data tidak tersimpan?**
- Cek permission file `data4.json`
- Pastikan tidak ada error di console

---

**Dibuat untuk Aplikasi Map Suroboyo**
*Dokumentasi ini menjelaskan cara kerja internal aplikasi dengan bahasa yang mudah dipahami*
