import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
from matplotlib.patches import Rectangle, Circle


def generate_grid_image(rows, cols, lines, line_colors, shapes):
    # Создаем изображение и оси
    fig, ax = plt.subplots()

    # Создаем сетку
    for i in range(1, rows):
        ax.axhline(i, color='black', lw=0.5)
    for j in range(1, cols):
        ax.axvline(j, color='black', lw=0.5)

    # Убираем оси
    ax.axis('off')

    # Устанавливаем размер изображения
    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)

    # Рисуем линии по заданным координатам
    # for line in lines:
    #     x1, y1, x2, y2 = line
    #     ax.plot([x1, x2], [y1, y2], color='blue', lw=2)
    rect = ''
    line_objects = []
    for line, color in zip(lines, line_colors):
        x1, y1, x2, y2 = line
        line_obj = Line2D([x1, x2], [y1, y2], color=color, lw=2)
        ax.add_line(line_obj)
        line_objects.append(line_obj)
    for shape in shapes:
        shape_type = shape[0]
        shape_params = shape[1:]

        if shape_type == 'rectangle':
            x, y, width, height, color = shape_params
            rect = Rectangle((x, y), width, height, color=color)
            ax.add_patch(rect)
        elif shape_type == 'circle':
            x, y, radius, color = shape_params
            circle = Circle((x, y), radius, color=color)
            ax.add_patch(circle)
    # Показываем изображение
    plt.show()
    return rect


lines = [
    [1, 2, 5, 1],  # Линия от (1,1) до (5,1)
    [3, 2, 3, 4],  # Линия от (3,2) до (3,4)
    [2, 4, 6, 4]   # Линия от (2,4) до (6,4)
]

line_colors = ['blue', 'red', 'green']

# Задаем размеры сетки
rows = 100
cols = 100

shapes = [
    ['rectangle', 1, 1, 2, 2, 'blue'],  # Прямоугольник
    ['circle', 4, 3, 1, 'red'],          # Круг
    ['rectangle', 2, 4, 3, 1, 'green']   # Еще прямоугольник
]

# Генерируем изображение сетки
rect = generate_grid_image(rows, cols, lines, line_colors, shapes)
rect.set_color('black')
plt.show()
