import tkinter as tk
from tkinter import Canvas

class GridEditor:
    def __init__(self, root, rows, cols):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.cell_size = 50
        self.shapes = []
        self.start_x = None
        self.start_y = None

        self.canvas = Canvas(self.root, width=cols * self.cell_size, height=rows * self.cell_size, bg='white')
        self.canvas.pack()

        # Создаем сетку
        for i in range(1, rows):
            self.canvas.create_line(i * self.cell_size, 0, i * self.cell_size, rows * self.cell_size, fill='black')
        for j in range(1, cols):
            self.canvas.create_line(0, j * self.cell_size, cols * self.cell_size, j * self.cell_size, fill='black')

        # Меню объектов
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.rectangle_button = tk.Button(self.menu_frame, text="Прямоугольник", command=self.add_rectangle)
        self.rectangle_button.pack()

        self.circle_button = tk.Button(self.menu_frame, text="Круг", command=self.add_circle)
        self.circle_button.pack()

        # Привязываем обработчики для перетаскивания
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)

    def add_rectangle(self):
        if self.start_x is not None and self.start_y is not None:
            x, y = self.snap_to_grid(self.start_x, self.start_y)
            rect = self.canvas.create_rectangle(x, y, x + self.cell_size, y + self.cell_size, fill='blue')
            self.shapes.append(('rectangle', rect))

    def add_circle(self):
        if self.start_x is not None and self.start_y is not None:
            x, y = self.snap_to_grid(self.start_x, self.start_y)
            circle = self.canvas.create_oval(x, y, x + self.cell_size, y + self.cell_size, fill='red')
            self.shapes.append(('circle', circle))

    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.selected_shape = None

        # Находим объект под мышкой
        for shape_type, shape_id in self.shapes:
            if self.canvas.coords(shape_id)[0] <= event.x <= self.canvas.coords(shape_id)[2] and \
                    self.canvas.coords(shape_id)[1] <= event.y <= self.canvas.coords(shape_id)[3]:
                self.selected_shape = shape_id
                break

    def on_drag(self, event):
        if self.selected_shape:
            dx = event.x - self.start_x
            dy = event.y - self.start_y
            self.canvas.move(self.selected_shape, dx, dy)
            self.start_x = event.x
            self.start_y = event.y

    def snap_to_grid(self, x, y):
        # Привязка к ближайшей сетке
        row = y // self.cell_size
        col = x // self.cell_size
        snapped_x = col * self.cell_size
        snapped_y = row * self.cell_size
        return snapped_x, snapped_y


# Создаем основное окно
root = tk.Tk()
root.title("Редактор сетки")

# Задаем размеры сетки
rows = 10
cols = 10

# Создаем редактор сетки
editor = GridEditor(root, rows, cols)

# Запускаем основной цикл обработки событий
root.mainloop()
