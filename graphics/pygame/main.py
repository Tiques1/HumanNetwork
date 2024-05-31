import pygame
import sys

# Инициализация Pygame
pygame.init()

# Настройки окна
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
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
class Neuron:
    def __init__(self, x, y, color=WHITE):
        self.x = x
        self.y = y
        self.color = color
        self.radius = 20
        self.connections = []

    def draw(self, screen, camera_x, camera_y, scale):
        neuron_pos = (camera_x + self.x * scale, camera_y + self.y * scale)
        pygame.draw.circle(screen, self.color, (int(neuron_pos[0]), int(neuron_pos[1])), int(self.radius * scale))
        for connection in self.connections:
            connection_pos = (camera_x + connection.x * scale, camera_y + connection.y * scale)
            pygame.draw.line(screen, self.color, (int(neuron_pos[0]), int(neuron_pos[1])), (int(connection_pos[0]), int(connection_pos[1])), int(2 * scale))

    def add_connection(self, neuron):
        self.connections.append(neuron)

    def change_color(self, color):
        self.color = color

# Функции
def get_neuron_at_position(neurons, pos, camera_x, camera_y, scale):
    scaled_pos = ((pos[0] - camera_x) / scale, (pos[1] - camera_y) / scale)
    for neuron in neurons:
        if (neuron.x - scaled_pos[0]) ** 2 + (neuron.y - scaled_pos[1]) ** 2 <= (neuron.radius * scale) ** 2:
            return neuron
    return None

# Класс для действий над нейронами
class NeuronActions:
    def __init__(self):
        self.neurons = []
        self.selected_neuron = None
        self.dragging = False
        self.camera_dragging = False
        self.camera_x = 0
        self.camera_y = 0
        self.scale = 1.0
        self.last_mouse_pos = None

    def add_neuron(self, pos):
        neuron = Neuron((pos[0] - self.camera_x) / self.scale, (pos[1] - self.camera_y) / self.scale)
        self.neurons.append(neuron)

    def select_neuron(self, pos):
        self.selected_neuron = get_neuron_at_position(self.neurons, pos, self.camera_x, self.camera_y, self.scale)
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
            self.neurons.remove(self.selected_neuron)
            for neuron in self.neurons:
                if self.selected_neuron in neuron.connections:
                    neuron.connections.remove(self.selected_neuron)
            self.selected_neuron = None

    def add_connection(self, target_neuron):
        if self.selected_neuron and target_neuron:
            self.selected_neuron.add_connection(target_neuron)

    def change_selected_neuron_color(self, color):
        if self.selected_neuron:
            self.selected_neuron.change_color(color)

    def draw_neurons(self, screen):
        for neuron in self.neurons:
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

# Инициализация действий над нейронами
neuron_actions = NeuronActions()

# Основной цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if event.button == 1:  # Левая кнопка мыши
                neuron = get_neuron_at_position(neuron_actions.neurons, pos, neuron_actions.camera_x, neuron_actions.camera_y, neuron_actions.scale)
                if neuron:
                    neuron_actions.select_neuron(pos)
                else:
                    neuron_actions.add_neuron(pos)

            elif event.button == 3:  # Правая кнопка мыши
                neuron = get_neuron_at_position(neuron_actions.neurons, pos, neuron_actions.camera_x, neuron_actions.camera_y, neuron_actions.scale)
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

    screen.fill(BLACK)
    neuron_actions.draw_neurons(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()
