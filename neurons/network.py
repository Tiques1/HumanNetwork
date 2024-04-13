import time

from neurons.neuron import Neuron
import asyncio


class Network:
    def __init__(self):
        #  replace axons and dendrites with it
        self.neurons: {Neuron: [Neuron]} = {}

    # first to second (one way communication)
    def link(self, n1, n2):
        self.neurons[n1].append(n2)

    def add(self, n: Neuron):
        self.neurons[n] = []

    async def maincycle(self):
        while True:
            for neuron in self.neurons.keys():
                neuron.step()
                tm = neuron.synapse
                neuron.synapse[0] = neuron.synapse[0] * 0.1
                neuron.synapse[1] = neuron.synapse[0] * 0.1
                amount = len(self.neurons[neuron])
                for dendrite in self.neurons[neuron]:
                    dendrite.dendrites((tm[0]/amount, tm[1]/amount))

            for neuron in self.neurons.keys():
                neuron.last_state = neuron.current_state

            time.sleep(0.01)


async def main():
    net = Network()
    asyncio.create_task(net.maincycle())
    n1 = Neuron('ПЕРВЫЙ')
    n2 = Neuron('ВТОРОЙ')
    net.add(n1)
    net.link(n1, n2)

if __name__ == '__main__':
    asyncio.run(main())
