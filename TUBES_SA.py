import tkinter as tk 
from tkinter import messagebox 
import time 

mazes = {
    "Maze 1": [
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,1],
        [1,0,1,1,1,0,1,0,1,0,1,1,1,1,1,1,0,1,0,1],
        [1,0,0,0,1,0,1,0,1,0,0,0,0,0,0,1,0,1,0,1],
        [1,1,1,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,0,1],
        [1,0,1,0,0,0,1,0,0,0,0,1,0,1,0,1,0,1,0,1],
        [1,0,1,0,1,1,1,1,1,1,0,1,0,1,0,1,0,1,0,1],
        [1,0,1,0,0,0,0,0,1,0,0,0,0,1,0,0,0,1,0,1],
        [1,0,1,1,1,1,1,0,0,0,1,1,0,1,0,1,1,1,0,1],
        [1,0,0,0,0,0,1,1,1,1,1,0,0,1,0,0,0,1,0,1],
        [1,1,1,0,1,1,1,0,0,0,0,0,1,1,1,1,1,1,0,0],
        [1,0,0,0,0,0,0,0,1,0,1,1,0,1,0,1,0,1,1,1],
        [1,0,1,1,1,1,1,1,1,0,1,0,0,0,0,1,0,1,0,1],
        [1,0,1,0,0,0,0,0,1,0,0,0,1,0,1,1,0,0,0,1],
        [1,0,0,0,1,1,1,0,1,0,1,0,1,1,0,0,0,1,1,1],
        [0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,1,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    ],
    "Maze 2": [
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,1],
        [1,1,1,0,1,0,1,0,1,1,1,1,0,1,1,1,0,1,0,1],
        [1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,1,0,1,0,1],
        [1,1,1,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,0,1],
        [1,0,0,0,1,0,1,0,0,0,0,1,0,1,0,1,0,1,0,1],
        [1,0,1,0,1,1,1,1,1,1,0,1,0,1,0,1,0,1,0,1],
        [1,0,1,0,0,0,0,0,1,0,0,0,0,1,0,0,0,1,0,1],
        [1,0,1,1,1,1,1,0,0,0,1,1,0,1,0,1,1,1,0,1],
        [1,0,0,0,0,0,1,1,0,1,1,1,0,1,0,0,0,1,0,1],
        [1,1,1,0,1,1,1,0,0,0,0,0,0,0,0,1,1,1,0,0],
        [1,0,0,0,0,0,0,0,1,0,1,1,1,0,1,1,0,1,1,1],
        [1,0,1,1,0,1,1,1,1,0,1,0,0,0,0,1,0,1,0,1],
        [1,0,0,1,0,1,0,0,1,0,1,0,1,0,1,1,0,0,0,1],
        [1,1,1,1,0,1,1,0,1,0,1,1,1,0,1,1,0,1,1,1],
        [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    ],
}

def solve_maze_backtracking(maze, start, end, app):
    def is_valid_move(x, y):
        return 0 <= x < len(maze[0]) and 0 <= y < len(maze) and maze[y][x] == 0

    def backtrack(x, y, path):
        if (x, y) == end:
            path.append((x, y))
            return True
        if is_valid_move(x, y):
            path.append((x, y))
            app.update_canvas(x, y, "blue", delay=20)  
            maze[y][x] = 2  
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                if backtrack(x + dx, y + dy, path):
                    return True
            path.pop() 
            app.update_canvas(x, y, "red", delay=20)  
            maze[y][x] = 0 
        return False

    path = []
    if backtrack(start[0], start[1], path):
        return True, path
    return False, []

def solve_maze_branch_and_bound(maze, start, end, app):
    from queue import PriorityQueue

    def heuristic(x, y):
        return abs(x - end[0]) + abs(y - end[1])

    pq = PriorityQueue()
    pq.put((0 + heuristic(*start), 0, start, []))
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    visited = set()

    while not pq.empty():
        _, cost, (x, y), path = pq.get()
        if (x, y) in visited:
            continue
        path.append((x, y))
        app.update_canvas(x, y, "blue", delay=20) 
        if (x, y) == end:
            return True, path
        visited.add((x, y))
        maze[y][x] = 2  
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze[0]) and 0 <= ny < len(maze) and maze[ny][nx] == 0:
                pq.put((cost + 1 + heuristic(nx, ny), cost + 1, (nx, ny), path[:]))
    return False, []

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Labirin solver")

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack()
        self.label = tk.Label(self.main_frame, text="Pilih Labirin:")
        self.label.pack(pady=10)

        self.maze_var = tk.StringVar(value="Maze 1")
        self.maze_menu = tk.OptionMenu(self.main_frame, self.maze_var, *mazes.keys())
        self.maze_menu.pack(pady=10)

        self.maze_display = tk.Canvas(self.main_frame, width=300, height=300)
        self.maze_display.pack(pady=10)

        self.update_maze_display()

        self.start_button = tk.Button(self.main_frame, text="Mulai", command=self.start_maze_app)
        self.start_button.pack(pady=10)

        self.exit_button = tk.Button(self.main_frame, text="Keluar", command=self.root.quit)
        self.exit_button.pack(pady=10)

        self.maze_var.trace_add("write", self.update_maze_display)

    def update_maze_display(self, *args):
        self.maze_display.delete("all")
        selected_maze = self.maze_var.get()
        maze = mazes[selected_maze]
        cell_size = min(300 // len(maze[0]), 300 // len(maze))
        for y in range(len(maze)):
            for x in range(len(maze[0])):
                color = "white" if maze[y][x] == 0 else "black"
                self.maze_display.create_rectangle(
                    x * cell_size, y * cell_size,
                    (x + 1) * cell_size, (y + 1) * cell_size,
                    fill=color
                )

    def start_maze_app(self):
        selected_maze = self.maze_var.get()
        maze = mazes[selected_maze]
        self.main_frame.destroy()
        MazeApp(self.root, maze).run()

class MazeApp:
    def __init__(self, root, maze):
        self.root = root
        self.root.title("Labirin solver")
        self.canvas = tk.Canvas(self.root, width=500, height=500)
        self.canvas.pack()

        self.maze = maze
        self.original_maze = [row[:] for row in self.maze]  
        self.width = len(maze[0])
        self.height = len(maze)
        self.cell_size = 500 // self.width  
        self.start = (0, 15)
        self.end = (self.width - 1, self.height - 7)

        self.draw_maze()
        self.solve_backtracking_button = tk.Button(self.root, text="Selesaikan dengan Backtracking", command=self.solve_maze_backtracking)
        self.solve_backtracking_button.pack()
        self.solve_branch_and_bound_button = tk.Button(self.root, text="Selesaikan dengan Branch and Bound", command=self.solve_maze_branch_and_bound)
        self.solve_branch_and_bound_button.pack()
        self.reset_button = tk.Button(self.root, text="Reset Labirin", command=self.reset_maze)
        self.reset_button.pack()
        self.go_back_button = tk.Button(self.root, text="Kembali", command=self.go_back)
        self.go_back_button.pack()

    def draw_maze(self):
        self.canvas.delete("all")
        for y in range(self.height):
            for x in range(self.width):
                color = "white" if self.maze[y][x] == 0 else "black"
                self.canvas.create_rectangle(
                    x * self.cell_size, y * self.cell_size,
                    (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                    fill=color
                )
        self.canvas.create_rectangle(
            self.start[0] * self.cell_size, self.start[1] * self.cell_size,
            (self.start[0] + 1) * self.cell_size, (self.start[1] + 1) * self.cell_size,
            fill="green"
        )
        self.canvas.create_rectangle(
            self.end[0] * self.cell_size, self.end[1] * self.cell_size,
            (self.end[0] + 1) * self.cell_size, (self.end[1] + 1) * self.cell_size,
            fill="red"
        )

    def update_canvas(self, x, y, color, delay=0):
        self.canvas.create_rectangle(
            x * self.cell_size, y * self.cell_size,
            (x + 1) * self.cell_size, (y + 1) * self.cell_size,
            fill=color
        )
        self.canvas.update_idletasks()
        if delay > 0:
            self.canvas.after(delay)

    def solve_maze_backtracking(self):
        self.maze = [row[:] for row in self.original_maze] 
        self.draw_maze()
        start_time = time.time()  
        solution_found, path = solve_maze_backtracking(self.maze, self.start, self.end, self)
        end_time = time.time() 
        elapsed_time = end_time - start_time  
        if solution_found:
            for x, y in path:
                self.update_canvas(x, y, "green", delay=20)
            messagebox.showinfo("Labirinth Solver", f"Solusi Ditemukan!\nTotal waktu : {elapsed_time:.2f} detik")
        else:
            messagebox.showinfo("Labirinth Solver", f"Tidak ditemukan solusi.\nTotal waktu : {elapsed_time:.2f} detik")

    def solve_maze_branch_and_bound(self):
        self.maze = [row[:] for row in self.original_maze]  
        self.draw_maze()
        start_time = time.time() 
        solution_found, path = solve_maze_branch_and_bound(self.maze, self.start, self.end, self)
        end_time = time.time() 
        elapsed_time = end_time - start_time 
        if solution_found:
            for x, y in path:
                self.update_canvas(x, y, "green", delay=20)
            messagebox.showinfo("Labirin Solver", f"Solusi ditemukan!\nTotal waktu: {elapsed_time:.2f} detik")
        else:
            messagebox.showinfo("Labirin Solver", f"Tidak ditemukan solusi.\nTotal waktu: {elapsed_time:.2f} detik")

    def reset_maze(self):
        self.maze = [row[:] for row in self.original_maze]  
        self.draw_maze()

    def go_back(self):
        self.root.destroy()
        root = tk.Tk()
        main_menu = MainMenu(root)
        root.mainloop()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    main_menu = MainMenu(root)
    root.mainloop()
