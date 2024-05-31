import threading
import time

from neurons.neuron import Neuron
import asyncio


class Network:
    def __init__(self):
        #  replace axons and dendrites with it
        self.neurons: {Neuron: [Neuron]} = {}
        self.run = False

    # first to second (one way communication)
    def link(self, n1, n2):
        self.neurons[n1].append(n2)

    def add(self, n: Neuron):
        self.neurons[n] = []

    def maincycle(self):
        c=0
        while self.run:
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
            c+=1
            print(f'-----------{c}------------')


def main():
    net = Network()
    # asyncio.create_task(net.maincycle())
    net.run = True
    threading.Thread(target=net.maincycle).start()
    n1 = Neuron('ПЕРВЫЙ')
    n2 = Neuron('ВТОРОЙ')
    net.add(n1)
    net.add(n2)
    net.link(n1, n2)

if __name__ == '__main__':
    # asyncio.run(main())
    main()
