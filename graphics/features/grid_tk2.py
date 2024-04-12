import tkinter as tk
from tkinter import Canvas


class GridEditor:
    def __init__(self, root, rows, cols):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.shapes = []

        self.canvas = Canvas(self.root, width=cols * 50, height=rows * 50, bg='white')
        self.canvas.pack()

        # Создаем сетку
        for i in range(1, rows):
            self.canvas.create_line(i * 50, 0, i * 50, rows * 50, fill='black')
        for j in range(1, cols):
            self.canvas.create_line(0, j * 50, cols * 50, j * 50, fill='black')

        # Меню объектов
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(side=tk.TOP, fill=tk.X)

        self.rectangle_button = tk.Button(self.menu_frame, text="Прямоугольник", command=self.add_rectangle)
        self.rectangle_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.circle_button = tk.Button(self.menu_frame, text="Круг", command=self.add_circle)
        self.circle_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Привязываем обработчики для перетаскивания
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)

        # Обработчики для перемещения по сетке
        self.canvas.bind("<Up>", self.move_up)
        self.canvas.bind("<Down>", self.move_down)
        self.canvas.bind("<Left>", self.move_left)
        self.canvas.bind("<Right>", self.move_right)

        # Начальные координаты
        self.start_x = 0
        self.start_y = 0
        self.selected_shape = None

    def add_rectangle(self):
        rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x + 50, self.start_y + 50,
                                            fill='blue')
        self.shapes.append(('rectangle', rect))

    def add_circle(self):
        circle = self.canvas.create_oval(self.start_x, self.start_y, self.start_x + 50, self.start_y + 50, fill='red')
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

    def move_up(self, event):
        self.canvas.move(tk.ALL, 0, -50)

    def move_down(self, event):
        self.canvas.move(tk.ALL, 0, 50)

    def move_left(self, event):
        self.canvas.move(tk.ALL, -50, 0)

    def move_right(self, event):
        self.canvas.move(tk.ALL, 50, 0)


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
