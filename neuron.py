class Neuron:
    def __init__(self):
        self.__treshold = 10  # treshold of activation
        self.__returnablity = 0.1  # percent of remaining transmitters
        self.__reproductivity = {'activator': 3,
                                 'ingibitor': 1}  # amount of transmitters + on each step
        self.__transmitters = {'activator': 0,
                               'ingibitor': 0}  # amount of transmitters, contains by neuron
        self.__dendrites = [(0, 0)]  # coordinates of dendrites
        self.__axons = [(0, 0)]  # coordinate of axons
        self.__signal_speed = 0  # the less, the faster signal will be sent
        self.__steps_to_activation = 0  # if 0, neuron ready to send signal. -=1 on each step
        self.__genom = {'test': 1}  # define how many neurotransmitters will be produced in dependece of input
        self.__input_transmitters = {'activator': 0,
                                     'ingibitor': 0}  # how many transmitters in synapse

    def input(self, transmitters):
        pass

    #  produce transmitters, plus remainings, handle input, move
    def step(self, transmitters):

        if self.__steps_to_activation == 0:
            self.__steps_to_activation = self.__signal_speed

            return map(lambda x: x/len(self.__axons), self.__transmitters.values())
        else:
            self.__steps_to_activation -= 1
