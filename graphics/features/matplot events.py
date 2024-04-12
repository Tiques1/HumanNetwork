import numpy as np
import matplotlib.pyplot as plt

# Создаем данные для графиков
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

# Создаем график
fig, ax = plt.subplots()
line1, = ax.plot(x, y1, label='sin(x)', picker=10)  # picker определяет радиус области выбора
line2, = ax.plot(x, y2, label='cos(x)', picker=10)
lines = [line1, line2]

# Функция для подсветки графика при нажатии
def on_pick(event):
    # Получаем выбранный объект (линию)
    line = event.artist
    # Изменяем цвет выбранной линии
    if line.get_picker():
        selected = not line.get_alpha()
        line.set_alpha(1.0 if selected else 0.5)
        fig.canvas.draw_idle()

# Связываем функцию с событием "pick_event"
fig.canvas.mpl_connect('pick_event', on_pick)

# Добавляем легенду
ax.legend()

plt.show()
