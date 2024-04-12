class Neuron:
    def __init__(self, a: (()), b: (())):
        self.treshold = 10  # treshold of activation
        self.returnablity = 0.1  # percent of remaining transmitters
        self.reproductivity = {'activator': 3,
                               'ingibitor': 1}  # amount of transmitters + on each step
        self.transmitters = {'activator': 0,
                             'ingibitor': 0}  # amount of transmitters, contains by neuron
        self.dendrites = a  # coordinates of dendrites e.g. ((0, 1), (0, 2))
        self.axons = b  # coordinate of axons e.g. ((2, 3), (1, 2))
        self.signal_speed = 0  # the less, the faster signal will be sent
        self.steps_to_activation = 0  # if 0, neuron ready to send signal. -=1 on each step
        self.genom = {'test': 1}  # define how many neurotransmitters will be produced in dependece of input
        self.current_state = {'activator': 0,
                              'ingibitor': 0}  # how many transmitters in synapse. before calculations complete
        self.last_state = {'activator': 0,
                           'ingibitor': 0}  # after calculations

    def input(self, transmitters):
        pass

    #  produce transmitters, plus remainings, handle input, move
    def step(self, transmitters):

        if self.steps_to_activation == 0:
            self.steps_to_activation = self.signal_speed

            return map(lambda x: x/len(self.axons), self.transmitters.values())
        else:
            self.steps_to_activation -= 1
