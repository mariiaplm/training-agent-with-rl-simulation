#The world the agent lives in: state, rules, and rewards
# Knows consequences only; never decides anything
#Actions: 0 = up, 1 = down, 2 = stay / open doors.

import random

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
        return self.current_floor, tuple(self.calls), tuple(self.destination)

    def step(self, action):
        reward = 0.0
        delivered = 0
        boarded = 0
        self.steps += 1

        if action == 0 and self.current_floor < self.n_floors - 1:
            self.current_floor += 1
            reward -= 0.1
        elif action == 1 and self.current_floor > 0:
            self.current_floor -= 1
            reward -= 0.1
        elif action == 2:
            floor = self.current_floor
            if self.destination[floor]:
                self.destination[floor] = False
                reward += 10.0
                delivered += 1
            if self.calls[floor]:
                self.calls[floor] = False
                reward += 1.0
                boarded += 1
                random_floor = self._random_other_floor(floor)
                self.destination[random_floor] = True


        self.current_floor = max(0, min(self.n_floors - 1, self.current_floor))

        self._spawn_passengers()
        reward -= 1.0 * sum(self.calls)
        reward -= 0.5 * sum(self.destination)
        done = self.steps >= self.max_steps

        info = {
            "delivered": delivered,
            "boarded": boarded,
            "waiting": sum(self.calls),
            "onboard": sum(self.destination)}

        return self.get_state(), reward, done, info

    def _spawn_passengers(self):
        for floor in range(self.n_floors):
            if not self.calls[floor]:
                if random.random() < self.arrival_rate:
                    self.calls[floor] = True


    def _random_other_floor(self, floor):
        new_list = [f for f in range(self.n_floors) if f != floor]
        return random.choice(new_list)

    def render(self):
        lines = []
        for floor in reversed(range(self.n_floors)):
            car = "[==]" if floor == self.current_floor else "    "
            call = "C" if self.calls[floor] else "."
            dest = "D" if self.destination[floor] else "."
            lines.append(f"{floor} {car} call:{call} dest:{dest}")
        lines.append(f"tick {self.steps}/{self.max_steps}")
        return "\n".join(lines)












