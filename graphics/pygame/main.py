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

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        for connection in self.connections:
            pygame.draw.line(screen, self.color, (self.x, self.y), (connection.x, connection.y), 2)

    def add_connection(self, neuron):
        self.connections.append(neuron)

    def change_color(self, color):
        self.color = color

class NeuronActions:
    def __init__(self):
        self.neurons = []
        self.selected_neuron = None
        self.dragging = False

    def add_neuron(self, pos):
        neuron = Neuron(pos[0], pos[1])
        self.neurons.append(neuron)

    def select_neuron(self, pos):
        self.selected_neuron = get_neuron_at_position(self.neurons, pos)
        if self.selected_neuron:
            self.dragging = True

    def deselect_neuron(self):
        self.dragging = False

    def move_neuron(self, pos):
        if self.dragging and self.selected_neuron:
            self.selected_neuron.x = pos[0]
            self.selected_neuron.y = pos[1]

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
            neuron.draw(screen)
        if self.selected_neuron:
            pygame.draw.circle(screen, HIGHLIGHT, (self.selected_neuron.x, self.selected_neuron.y), self.selected_neuron.radius, 3)


# Функции
def draw_neurons(neurons, screen, selected_neuron):
    for neuron in neurons:
        neuron.draw(screen)
    if selected_neuron:
        pygame.draw.circle(screen, HIGHLIGHT, (selected_neuron.x, selected_neuron.y), selected_neuron.radius, 3)

def get_neuron_at_position(neurons, pos):
    for neuron in neurons:
        if (neuron.x - pos[0]) ** 2 + (neuron.y - pos[1]) ** 2 <= neuron.radius ** 2:
            return neuron
    return None

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
                neuron = get_neuron_at_position(neuron_actions.neurons, pos)
                if neuron:
                    neuron_actions.select_neuron(pos)
                else:
                    neuron_actions.add_neuron(pos)

            elif event.button == 3:  # Правая кнопка мыши
                neuron = get_neuron_at_position(neuron_actions.neurons, pos)
                if neuron:
                    neuron_actions.add_connection(neuron)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Левая кнопка мыши
                neuron_actions.deselect_neuron()

        elif event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            neuron_actions.move_neuron(pos)

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

    screen.fill(BLACK)
    neuron_actions.draw_neurons(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()