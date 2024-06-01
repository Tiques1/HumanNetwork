from time import perf_counter_ns as pcns


class Neuron:
    def __init__(self, name):
        self.name = name
        self.treshold = 10  # treshold of activation
        self.returnablity = 0.1  # percent of remaining transmitters
        self.speed = 5  # the less, the faster signal will be sent after activation
        self.recovery = 5  # if 0, neuron ready to send signal. -=1 on each step after

        self.sta = 5  # sta - steps to activation. Set > 0 when created to autostart
        self.str = 0  # str - steps to recovery

        # outer tm
        self.dendrite = [0, 0]  # recieve from another synaps
        self.synapse = [0, 0]  # send to another neuron and reset to zero

        # inner tm
        self.reproductivity = [5, -0.1]  # amount of transmitters + on each step
        self.accumulated = [0, 0]  # move to synapse and set accumulated * returnability

        self.current_state = [0, 0]  # how many transmitters in synapse; before calculations complete
        self.last_state = [0, 0]  # after calculations; [activator, ingibitor]

    def step(self):
        self.accumulated[0] += self.reproductivity[0]
        self.accumulated[1] += self.reproductivity[1]
        if self.str > 0:
            print(pcns(), self.name, 'ВОССТАНАВЛИВАЮСЬ')
            self._recovery_state()

            self.str -= 1
        elif self.sta == 1:
            print(pcns(), self.name, 'ВЫБРАСЫВАЮ')
            self._dropping_state()

            self.sta = 0
            self.synapse[0] += self.accumulated[0]
            self.synapse[1] += self.accumulated[1]
            self.accumulated[0] = self.accumulated[0] * self.returnablity
            self.accumulated[1] = self.accumulated[1] * self.returnablity
            self.str = self.recovery
        elif self.sta > 0:
            print(pcns(), self.name, 'ПЕРЕДАЮ')
            self._givinig_state()

            self.sta -= 1
        elif self.last_state[0] + self.last_state[1] > self.treshold:
            print(pcns(), self.name, 'АКТИВИРУЮСЬ')
            self._activating_state()

            self.current_state = [0, 0]
            self.sta = self.speed
        else:
            print(pcns(), self.name, 'НАКАПЛИВАЮ')
            self._collecting_state()

            self.current_state[0] += self.dendrite[0]
            self.current_state[1] += self.dendrite[1]
            self.dendrite[0] = 0
            self.dendrite[1] = 0

    def dendrites(self, tm):
        print(pcns(), self.name, 'ПРИНИМАЮ')
        self._getting_state()

        self.dendrite[0] += tm[0]
        self.dendrite[1] += tm[1]

    def _recovery_state(self):
        pass

    def _dropping_state(self):
        pass

    def _givinig_state(self):
        pass

    def _activating_state(self):
        pass

    def _collecting_state(self):
        pass

    def _getting_state(self):
        pass
