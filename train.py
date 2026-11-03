import random
import pickle #extension that converts python objects into bytes
from collections import defaultdict

from elevator_env import ElevatorEnv

ALPHA = 0.1 #learning rate
GAMMA = 0.95 #discounted reward
EPSILON_START = 1.0 #begin fully random
EPSILON_MIN = 0.05 #never stop exploring entirely
EPSILON_DECAY = 0.9995 #multiply epsilon by this each episode
EPISODES = 20000
N_FLOORS = 5
MAX_STEPS = 200
ARRIVAL_RATE = 0.05

q_table = defaultdict(lambda: [0.0, 0.0, 0.0])

def choose_action(state, epsilon):
    if random.random() < epsilon:
        return random.randrange(3)
    else:
        values = q_table[state]
    return values.index(max(values))

def update(state, action, reward, next_state):
    curr_estimate = q_table[state][action]
    best_value_available = max(q_table[next_state])
    target = reward + GAMMA * best_value_available
    q_table[state][action] = curr_estimate + ALPHA * (target - q_table[state][action])

def train():
    epsilon = EPSILON_START
    env = ElevatorEnv(N_FLOORS, MAX_STEPS, ARRIVAL_RATE)
    for episode in range(EPISODES):
        state = env.reset()
        total_reward = 0.0
        done = False
        while not done:
            action = choose_action(state, epsilon)
            next_state, reward, done, info = env.step(action)
            update(state, action, reward, next_state)
            state = next_state
            total_reward += reward
        epsilon = max(EPSILON_MIN, EPSILON_DECAY * epsilon)
        if episode % 500 == 0:
            print(f"episode: {episode} epsilon {epsilon:.3f} reward{total_reward:.1f}")
    return q_table

def save_q_table(path="q_table.pkl"):
    with open(path, 'wb') as f:
        pickle.dump(dict(q_table), f)

def load_q_table(path="q_table.pkl"):
    with open(path, 'rb') as f:
        data = pickle.load(f)
    return defaultdict(lambda: [0.0, 0.0, 0.0], data)

if __name__ == "__main__":
    train()
    save_q_table()