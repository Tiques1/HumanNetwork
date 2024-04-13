from neurons.neuron import Neuron
import asyncio


class Network:
    def __init__(self):
        #  replace axons and dendrites with it
        self.neurons: {Neuron: [Neuron]} = {}

    def link(self, n1, n2):
        self.neurons[n1].append(n2)

    def add(self):
        n = Neuron(

        )
        self.neurons[n] = []
        return n

    async def maincycle(self):
        while True:
            for i in self.neurons.keys():



async def main():
    net = Network()
    asyncio.create_task(net.maincycle())
    while True:
        await asyncio.sleep(1)
        print('world')

if __name__ == '__main__':
    asyncio.run(main())
