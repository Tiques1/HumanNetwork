from neuron import Neuron


class Network:
    def __init__(self, width, height):
        self.neurons = []

        # manually
        self.link()

    def link(self, a, b):
        self.neurons.append(
            Neuron(
                a, b
            )
        )




net = Network(10, 10)

