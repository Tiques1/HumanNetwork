import threading
import math
import pygame
import sys
import pickle
import tkinter as tk
from tkinter import filedialog

from neurons.neuron import Neuron as NaturalNeuron
from neurons.network import Network

# Инициализация Pygame
pygame.init()

# Настройки окна
width, height = 800, 600
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("Графический редактор нейронов")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
HIGHLIGHT = (255, 255, 255)

# Класс нейрона
class Neuron(NaturalNeuron):
    def __init__(self, x, y, color=WHITE):
        super().__init__(NaturalNeuron)
        
        self.x = x
        self.y = y
        self.color = color
        self.line_color = color
        self.radius = 20
        self.connections = []

    def draw_arrow(self, screen, start_pos, end_pos, color, scale):
        arrow_size = 10 * scale
        angle = math.atan2(end_pos[1] - start_pos[1], end_pos[0] - start_pos[0])
        pygame.draw.line(screen, color, end_pos, (end_pos[0] - arrow_size * math.cos(angle - math.pi / 6),
                                                   end_pos[1] - arrow_size * math.sin(angle - math.pi / 6)), int(2 * scale))
        pygame.draw.line(screen, color, end_pos, (end_pos[0] - arrow_size * math.cos(angle + math.pi / 6),
                                                   end_pos[1] - arrow_size * math.sin(angle + math.pi / 6)), int(2 * scale))

    def draw(self, screen, camera_x, camera_y, scale):
        neuron_pos = (camera_x + self.x * scale, camera_y + self.y * scale)
        pygame.draw.circle(screen, self.color, (int(neuron_pos[0]), int(neuron_pos[1])), int(self.radius * scale))
        for connection in self.connections:
            connection_pos = (camera_x + connection.x * scale, camera_y + connection.y * scale)
            # Найти направление от текущего нейрона к связанному нейрону
            dx = connection_pos[0] - neuron_pos[0]
            dy = connection_pos[1] - neuron_pos[1]
            distance = math.sqrt(dx ** 2 + dy ** 2)
            if distance > 0:  # Проверка, чтобы избежать деления на 0
                # Координаты начала линии на границе круга текущего нейрона
                start_pos = (int(neuron_pos[0] + dx * self.radius * scale / distance),
                             int(neuron_pos[1] + dy * self.radius * scale / distance))
                # Координаты конца линии на границе круга связанного нейрона
                end_pos = (int(connection_pos[0] - dx * connection.radius * scale / distance),
                           int(connection_pos[1] - dy * connection.radius * scale / distance))
                pygame.draw.line(screen, self.line_color, start_pos, end_pos, int(2 * scale))
                self.draw_arrow(screen, start_pos, end_pos, self.line_color, scale)

        # Отображение характеристик
        font = pygame.font.SysFont('Arial', 16)
        characteristics = f"sta: {self.sta}, str: {self.str}, dendrite: {round(self.dendrite[0], 2), round(self.dendrite[1], 2)}," \
                          f"accumulated: {round(self.accumulated[0], 2), round(self.accumulated[1], 2)}, " \
                          f"synapse: {round(self.synapse[0], 2), round(self.synapse[1], 2)}, " \
                          f"last: {round(self.last_state[0], 2), round(self.last_state[1], 2)}, " \
                          f"current: {round(self.current_state[0], 2), round(self.current_state[1], 2)}"
        text = font.render(characteristics, True, WHITE)
        screen.blit(text, (int(neuron_pos[0] + self.radius * scale + 5), int(neuron_pos[1] - self.radius * scale)))

    def add_connection(self, neuron):
        if neuron in self.connections:
            self.connections.remove(neuron)
        else:
            self.connections.append(neuron)

    def change_color(self, color):
        self.color = color

    # def _collecting_state(self):
    #     self.color = self.color_range()

    def _dropping_state(self):
        # self.color = WHITE
        self.line_color = (255, 215, 0)

    def _recovery_state(self):
        self.line_color = WHITE

    def color_range(self):
        value = sum(self.current_state)
        min_value = 0
        max_value = self.treshold

        # Нормируем значение в диапазон от 0 до 1
        normalized = (value - min_value) / (max_value - min_value)
        normalized = max(0, min(1, normalized))  # Ограничиваем диапазон от 0 до 1

        # Цвета в формате RGB
        white = (255, 255, 255)
        gold = (255, 215, 0)

        # Интерполяция цветов
        r = int(white[0] + (gold[0] - white[0]) * normalized)
        g = int(white[1] + (gold[1] - white[1]) * normalized)
        b = int(white[2] + (gold[2] - white[2]) * normalized)

        return (r, g, b)


# Функции
def get_neuron_at_position(neurons, pos, camera_x, camera_y, scale):
    scaled_pos = ((pos[0] - camera_x) / scale, (pos[1] - camera_y) / scale)
    for neuron in neurons:
        if (neuron.x - scaled_pos[0]) ** 2 + (neuron.y - scaled_pos[1]) ** 2 <= (neuron.radius * scale) ** 2:
            return neuron
    return None

# Класс для действий над нейронами
class NeuronActions:
    def __init__(self, network=Network()):
        self.network = network
        self.network.run = True
        threading.Thread(target=self.network.maincycle).start()

        self.selected_neuron = None
        self.dragging = False
        self.camera_dragging = False
        self.camera_x = 0
        self.camera_y = 0
        self.scale = 1.0
        self.last_mouse_pos = None

    def add_neuron(self, pos):
        neuron = Neuron((pos[0] - self.camera_x) / self.scale, (pos[1] - self.camera_y) / self.scale)
        self.network.add(neuron)

    def select_neuron(self, pos):
        self.selected_neuron = get_neuron_at_position(self.network.neurons.keys(), pos, self.camera_x, self.camera_y,
                                                      self.scale)
        if self.selected_neuron:
            self.dragging = True

    def deselect_neuron(self):
        self.dragging = False

    def move_neuron(self, pos):
        if self.dragging and self.selected_neuron:
            self.selected_neuron.x = (pos[0] - self.camera_x) / self.scale
            self.selected_neuron.y = (pos[1] - self.camera_y) / self.scale

    def delete_selected_neuron(self):
        if self.selected_neuron:
            self.network.neurons.pop(self.selected_neuron)
            for neuron in self.network.neurons.keys():
                if self.selected_neuron in neuron.connections:
                    neuron.connections.remove(self.selected_neuron)
            self.selected_neuron = None

    def add_connection(self, target_neuron):
        if self.selected_neuron and target_neuron:
            self.network.link(self.selected_neuron, target_neuron)
            self.selected_neuron.add_connection(target_neuron)

    def change_selected_neuron_color(self, color):
        if self.selected_neuron:
            self.selected_neuron.change_color(color)

    def draw_neurons(self, screen):
        for neuron in self.network.neurons.keys():
            neuron.draw(screen, self.camera_x, self.camera_y, self.scale)
        if self.selected_neuron:
            selected_pos = (self.camera_x + self.selected_neuron.x * self.scale, self.camera_y + self.selected_neuron.y * self.scale)
            pygame.draw.circle(screen, HIGHLIGHT, (int(selected_pos[0]), int(selected_pos[1])), int(self.selected_neuron.radius * self.scale), 3)

    def zoom(self, amount):
        self.scale += amount
        if self.scale < 0.1:
            self.scale = 0.1

    def move_camera(self, dx, dy):
        self.camera_x += dx
        self.camera_y += dy

    def start_camera_drag(self, pos):
        self.camera_dragging = True
        self.last_mouse_pos = pos

    def stop_camera_drag(self):
        self.camera_dragging = False

    def drag_camera(self, pos):
        if self.camera_dragging:
            dx = pos[0] - self.last_mouse_pos[0]
            dy = pos[1] - self.last_mouse_pos[1]
            self.move_camera(dx, dy)
            self.last_mouse_pos = pos

    def save_to_file(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.network, f)

    def load_from_file(self, filename):
        with open(filename, 'rb') as f:
            self.network.run = False
            self.network = pickle.load(f)
            threading.Thread(target=self.network.maincycle).start()

def choose_file():
    root = tk.Tk()
    root.withdraw()
    filename = filedialog.askopenfilename()
    return filename

if __name__ == "__main__":
    # Инициализация действий над нейронами
    neuron_actions = NeuronActions()

    # Выбор файла для загрузки
    filename = choose_file()
    if filename:
        neuron_actions.load_from_file(filename)
    else:
        print("Выберите файл для загрузки.")

    # Основной цикл
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if event.button == 1:  # Левая кнопка мыши
                    neuron = get_neuron_at_position(neuron_actions.network.neurons.keys(), pos, neuron_actions.camera_x,
                                                    neuron_actions.camera_y, neuron_actions.scale)
                    if neuron:
                        neuron_actions.select_neuron(pos)
                    else:
                        neuron_actions.add_neuron(pos)

                elif event.button == 3:  # Правая кнопка мыши
                    neuron = get_neuron_at_position(neuron_actions.network.neurons.keys(), pos, neuron_actions.camera_x,
                                                    neuron_actions.camera_y, neuron_actions.scale)
                    if neuron:
                        neuron_actions.add_connection(neuron)
                    else:
                        neuron_actions.start_camera_drag(pos)

                elif event.button == 4:  # Колесо мыши вверх (увеличение масштаба)
                    neuron_actions.zoom(0.1)

                elif event.button == 5:  # Колесо мыши вниз (уменьшение масштаба)
                    neuron_actions.zoom(-0.1)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Левая кнопка мыши
                    neuron_actions.deselect_neuron()
                elif event.button == 3:  # Правая кнопка мыши
                    neuron_actions.stop_camera_drag()

            elif event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                if neuron_actions.dragging:
                    neuron_actions.move_neuron(pos)
                if neuron_actions.camera_dragging:
                    neuron_actions.drag_camera(pos)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    neuron_actions.change_selected_neuron_color(RED)
                elif event.key == pygame.K_g:
                    neuron_actions.change_selected_neuron_color(GREEN)
                elif event.key == pygame.K_b:
                    neuron_actions.change_selected_neuron_color(BLUE)
                elif event.key == pygame.K_y:
                    neuron_actions.change_selected_neuron_color(YELLOW)
                elif event.key == pygame.K_DELETE:
                    neuron_actions.delete_selected_neuron()
                elif event.key == pygame.K_UP:
                    neuron_actions.move_camera(0, -10)
                elif event.key == pygame.K_DOWN:
                    neuron_actions.move_camera(0, 10)
                elif event.key == pygame.K_LEFT:
                    neuron_actions.move_camera(-10, 0)
                elif event.key == pygame.K_RIGHT:
                    neuron_actions.move_camera(10, 0)
                elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    filename = filedialog.asksaveasfilename(defaultextension=".pkl")
                    if filename:
                        neuron_actions.save_to_file(filename)

        screen.fill(BLACK)
        neuron_actions.draw_neurons(screen)
        pygame.display.flip()

    neuron_actions.network.run = False
    pygame.quit()
    sys.exit()
