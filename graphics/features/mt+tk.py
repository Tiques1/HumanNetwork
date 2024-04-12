import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.lines import Line2D

rows = 10
cols = 10
lines = [
    [1, 2, 5, 1],  # Линия от (1,1) до (5,1)
    [3, 2, 3, 4],  # Линия от (3,2) до (3,4)
    [2, 4, 6, 4]   # Линия от (2,4) до (6,4)
]

# Создаем данные для графиков
# x = np.linspace(0, 10, 100)
# y1 = np.sin(x)
# y2 = np.cos(x)


# Создаем функцию для отображения выбранного графика
def show_selected_graph(event):
    selection = listbox.curselection()  # Получаем индекс выбранного элемента
    if selection:
        idx = int(selection[0])  # Переводим индекс в целое число
        for i, line in enumerate(line_objects):
            if i == idx:
                line.set_visible(True)  # Показываем выбранный график
            else:
                line.set_visible(False)  # Скрываем остальные
        fig.canvas.draw_idle()


# Создаем график
fig = Figure(figsize=(6, 4))
ax = fig.add_subplot(111)

for i in range(1, rows):
    ax.axhline(i, color='black', lw=0.5)
for j in range(1, cols):
    ax.axvline(j, color='black', lw=0.5)

ax.axis('off')

ax.set_xlim(0, cols)
ax.set_ylim(0, rows)

line_objects = []
for line in lines:
    x1, y1, x2, y2 = line
    line_obj = Line2D([x1, x2], [y1, y2], lw=2)
    ax.add_line(line_obj)
    line_objects.append(line_obj)

# Создаем окно tkinter
root = tk.Tk()
root.title("Графики")

# Создаем виджет Canvas для отображения графика
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

# Создаем листбокс для списка графиков
listbox = tk.Listbox(root, selectmode=tk.SINGLE)
listbox.pack(side=tk.RIGHT, fill=tk.BOTH)

# Добавляем элементы в листбокс
for line in line_objects:
    listbox.insert(tk.END, str(line))


# Привязываем функцию к выбору элемента в листбоксе
listbox.bind("<<ListboxSelect>>", show_selected_graph)

# Показываем окно tkinter
root.mainloop()
