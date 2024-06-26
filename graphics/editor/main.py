import random
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from tkinter import Tk


class Window(Tk):
    def __init__(self, width, height):
        super().__init__()
        self.rows = width
        self.cols = height
        self.line_objects = []
        self.lines = [
            [1, 2, 5, 1],  # Линия от (1,1) до (5,1)
            [3, 2, 3, 4],  # Линия от (3,2) до (3,4)
            [2, 4, 6, 4]   # Линия от (2,4) до (6,4)
        ]
        # matplot graph
        self.fig = Figure(figsize=(6, 4))
        self.ax = self.fig.add_subplot(111)
        # Создаем виджет Canvas для отображения графика
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')
        # Создаем листбокс для списка графиков
        self.listbox = tk.Listbox(self, selectmode=tk.SINGLE, bg='lightblue')
        self.listbox.grid(column=2, row=0, sticky='nsew')

        self.title("Graphs")

        self._prepare()

    def add_line(self, event):
        x1, y1, x2, y2 = [random.randint(0, 50) for _ in range(0, 4)]
        line_obj = Line2D([x1, x2], [y1, y2], lw=2)
        self.ax.add_line(line_obj)
        self.listbox.insert(tk.END, str(line_obj))
        self.listbox.update()
        self.line_objects.append(line_obj)
        self.canvas.draw_idle()

    def _scroll_vert(self, value):
        a = int(self.scale.get())
        val = int(value)
        if a < 0 or a > self.cols:
            return
        else:
            self.ax.set_ylim(val-a//2, val+a//2)
        self.fig.canvas.draw_idle()

    def _scroll_horz(self, value):
        a = int(self.scale.get())
        val = int(value)
        if a < 0 or a > self.cols:
            return
        else:
            self.ax.set_xlim(val-a//2, val+a//2)
        self.fig.canvas.draw_idle()

    # Создаем функцию для отображения выбранного графика
    def _show_selected_graph(self, event):
        selection = self.listbox.curselection()  # Получаем индекс выбранного элемента
        if selection:
            idx = int(selection[0])  # Переводим индекс в целое число
            for i, line in enumerate(self.line_objects):
                if i == idx and line.get_visible() is False:
                    line.set_visible(True)
                elif i == idx:
                    line.set_visible(False)
            self.fig.canvas.draw_idle()

    def _prepare(self):
        for i in range(1, self.rows):
            self.ax.axhline(i, color='black', lw=0.1)
        for j in range(1, self.cols):
            self.ax.axvline(j, color='black', lw=0.1)

        self.ax.axis('off')

        self.grid_columnconfigure(0, weight=5)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=1)

        self.grid_rowconfigure(0, weight=10)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=5)

        for line in self.lines:
            x1, y1, x2, y2 = line
            line_obj = Line2D([x1, x2], [y1, y2], lw=2)
            self.ax.add_line(line_obj)
            self.line_objects.append(line_obj)

        for line in self.line_objects:
            self.listbox.insert(tk.END, str(line))

        # Создаем Frame для сетки
        frame = tk.Frame(self, bg="darkgray")
        frame.grid(row=2, column=0, sticky='nsew')

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_columnconfigure(2, weight=1)

        new_neuro_button = tk.Button(frame, text='Button1', width=10, height=2)
        new_neuro_button.grid(row=0, column=0, sticky='nw')
        new_neuro_button2 = tk.Button(frame, text='Button2', width=10, height=2)
        new_neuro_button2.grid(sticky='nsew', row=1, column=1)

        button = tk.Button(self, text='Create new')
        button.grid(column=2, row=1, sticky='nsew')

        # Привязываем функцию к выбору элемента в листбоксе
        self.listbox.bind("<<ListboxSelect>>", self._show_selected_graph)
        button.bind("<Button-1>", self.add_line)

        vert = tk.Scale(self, to=0, from_=self.rows, orient=tk.VERTICAL, command=self._scroll_vert)
        vert.set(self.cols)
        vert.grid(column=1, row=0, sticky='nsew')

        horz = tk.Scale(self, from_=0, to=self.rows, orient=tk.HORIZONTAL, command=self._scroll_horz)
        horz.set(self.rows)
        horz.grid(column=0, row=1, sticky='nsew')

        self.scale = tk.Entry(self)
        self.scale.grid(column=2, row=2)
        button = tk.Button(self, text='Zoom', command=lambda: (self._scroll_horz(horz.get()),
                                                               self._scroll_vert(vert.get())))
        button.grid(column=2, row=2, sticky='s')


if __name__ == '__main__':
    window = Window(50, 50)
    window.mainloop()
