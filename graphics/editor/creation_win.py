from tkinter import Tk, Label, Entry, Button
from neurons.neuron import Neuron
from neurons.network import Network


class Create(Tk):
    def __init__(self, network: Network):
        super().__init__()
        self.title('Create new')
        Label(self, text='Enter name:').pack()
        Entry(self).pack()

        Label(self, text='Enter point a:').pack()
        Entry(self).pack()

        Label(self, text='Enter point b:').pack()
        Entry(self).pack()

        Button(self, text='Create')

    def _create(self):
        pass


if __name__ == '__main__':
    network = Network(50, 50)
    create = Create(network)
    create.mainloop()
