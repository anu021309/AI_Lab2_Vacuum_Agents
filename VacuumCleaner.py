import tkinter as tk
import random

class VacuumRoomApp:
    def __init__(self, root, rows, cols, Vx, Vy):
        self.rows = rows
        self.cols = cols
        self.Vx = Vx
        self.Vy = Vy
        self.cell_size = 120
        self.total_cost = 0
        self.room = [[random.randint(0, 1) for _ in range(cols)] for _ in range(rows)]

        # Count total dirty cells at start
        self.total_dirt = sum(cell for row in self.room for cell in row)

        self.canvas = tk.Canvas(root, width=self.cols * self.cell_size, height=self.rows * self.cell_size + 40)
        self.canvas.pack()
        self.draw_room()

        root.after(1000, self.update)

    def GetStatus(self, x, y):
        return self.room[x][y]

    def GoalTest(self):
        return all(cell == 0 for row in self.room for cell in row)

    def draw_room(self):
        self.canvas.delete("all")
        for i in range(self.rows):
            for j in range(self.cols):
                x1 = j * self.cell_size
                y1 = i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                fill_color = "darkgray" if self.room[i][j] == 1 else "lightgray"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline="black")

                if i == self.Vx and j == self.Vy:
                    self.canvas.create_oval(x1 + 20, y1 + 20, x2 - 20, y2 - 20, fill="red")
                    self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text="V", fill="white", font=("Arial", 30, "bold"))
                else:
                    self.canvas.create_text(x1 + 20, y1 + 30, text=str(self.room[i][j]), font=("Arial", 20))

        # Show total cost and cost-to-dirt ratio
        ratio = self.total_cost / self.total_dirt if self.total_dirt > 0 else 0
        self.canvas.create_text(10, self.rows * self.cell_size + 20,
                                anchor="w",
                                text=f"Total Cost: {self.total_cost} | Cost / Dirt Ratio: {ratio:.2f}",
                                font=("Arial", 16, "bold"))

    def update(self):
        if self.GetStatus(self.Vx, self.Vy) == 1:
            self.room[self.Vx][self.Vy] = 0
            self.total_cost += 1  # suction cost
            ratio = self.total_cost / self.total_dirt if self.total_dirt > 0 else 0
            print(f"Cleaned ({self.Vx},{self.Vy}) | Total cost: {self.total_cost} | Ratio: {ratio:.2f}")

        elif not self.GoalTest():
            directions = [
                (-1, 0), (-1, 1), (0, 1), (1, 1),
                (1, 0), (1, -1), (0, -1), (-1, -1)
            ]
            moved = False
            for dx, dy in directions:
                new_x, new_y = self.Vx + dx, self.Vy + dy
                if 0 <= new_x < self.rows and 0 <= new_y < self.cols and self.room[new_x][new_y] == 1:
                    self.Vx, self.Vy = new_x, new_y
                    self.total_cost += 1  # move cost
                    ratio = self.total_cost / self.total_dirt if self.total_dirt > 0 else 0
                    print(f"Moved to ({self.Vx},{self.Vy}) | Total cost: {self.total_cost} | Ratio: {ratio:.2f}")
                    moved = True
                    break

            if not moved:
                for i in range(self.rows):
                    for j in range(self.cols):
                        if self.room[i][j] == 1:
                            dx = i - self.Vx
                            dy = j - self.Vy
                            step_x = 0 if dx == 0 else dx // abs(dx)
                            step_y = 0 if dy == 0 else dy // abs(dy)
                            self.Vx += step_x
                            self.Vy += step_y
                            self.total_cost += 1
                            ratio = self.total_cost / self.total_dirt if self.total_dirt > 0 else 0
                            print(f"Stepped toward ({i},{j}) now at ({self.Vx},{self.Vy}) | Total cost: {self.total_cost} | Ratio: {ratio:.2f}")
                            self.draw_room()
                            self.canvas.after(500, self.update)
                            return

        self.draw_room()

        if not self.GoalTest():
            self.canvas.after(500, self.update)
        else:
            ratio = self.total_cost / self.total_dirt if self.total_dirt > 0 else 0
            print(f"✅ All cells cleaned! Total cost: {self.total_cost} | Ratio: {ratio:.2f}")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Vacuum Cleaner Agent - 8 Directional with Cost and Ratio")

    x = 6
    y = 8
    Vx = 2
    Vy = 3

    app = VacuumRoomApp(root, x, y, Vx, Vy)
    root.mainloop()
