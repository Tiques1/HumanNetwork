import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy as np

# Создаем несколько графиков
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

fig, ax = plt.subplots()
ax.plot(x, y1, label='sin(x)')
ax.plot(x, y2, label='cos(x)')
ax.legend()

# Определяем функцию для переключения графиков
def switch_graphs(event):
    lines = ax.get_lines()
    for line in lines:
        visibility = line.get_visible()
        line.set_visible(not visibility)
    plt.draw()

# Создаем кнопку для переключения графиков
button = Button(plt.axes([0.8, 0.05, 0.1, 0.075]), 'Переключить')
button.on_clicked(switch_graphs)

plt.show()
