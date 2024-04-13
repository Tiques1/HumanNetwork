class Neuron:
    def __init__(self):
        self.treshold = 10  # treshold of activation
        self.returnablity = 0.1  # percent of remaining transmitters
        self.speed = 5  # the less, the faster signal will be sent after activation
        self.recovery = 5  # if 0, neuron ready to send signal. -=1 on each step after

        self.sta = self.recovery  # sta - steps to activation
        self.str = self.recovery  # str - steps to recovery

        self.reproductivity = {'activator': 3,
                               'ingibitor': 1}  # amount of transmitters + on each step

        self.synapse = [0, 0]
        self.accumulated = [0, 0]

        self.current_state = [0, 0]  # how many transmitters in synapse; before calculations complete
        self.last_state = [0, 0]  # after calculations; [activator, ingibitor]
        # Добавить в будущем функцию производства нейротрансмиттеров

    def step(self, tm):
        if self.str > 0:
            self.str -= 1
            return
        if self.sta == 1:
            self.sta = 0
            self.synapse[0] += self.accumulated[0]
            self.synapse[0] += self.accumulated[1]
            self.str = self.recovery
            return
        if self.sta > 0:
            self.sta -= 1
            return
        if self.current_state[0] + self.current_state[1] > self.treshold:
            self.sta = self.speed
            return

        self.current_state[0] += tm[0]
        self.current_state[1] += tm[1]



