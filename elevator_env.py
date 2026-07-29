#file that owns states, rules, and rewards

class ElevatorEnv:
    def __init__(self, n_floors, max_steps, arrival_rate):
        self.n_floors = n_floors
        self.max_steps = max_steps
        self.arrival_rate = arrival_rate
        self.current_floor = 0
        self.calls = []
        self.destination = []
        self.steps = 0
        self.reset()

    def reset(self):
        self.current_floor = 0
        self.calls = [False] * self.n_floors
        self.destination = [False] * self.n_floors
        self.steps = 0
        return self.get_state()

    def get_state(self):
        return (self.current_floor, tuple(self.calls), tuple(self.destination))

    def step(self, action):
        self.current_floor += 1
        self.steps += 1



