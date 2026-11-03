# Entry point: loads the trained Q-table and watches the agent run the elevator
# No exploration and no learning here; only uses the policy train.py produced

import time
from elevator_env import ElevatorEnv
from train import load_q_table, N_FLOORS, ARRIVAL_RATE

def run(steps = 50, delay = 0.3):
    q_table = load_q_table()
    env = ElevatorEnv(N_FLOORS, steps, ARRIVAL_RATE)
    state = env.reset()
    total = 0.0
    done = False

    while not done:
        values = q_table[state]
        action = values.index(max(values))
        state, reward, done, info = env.step(action)
        total += reward
        print(env.render())
        print(f"action: {action} reward: {reward:.1f} total: {total:.1f}\n")
        time.sleep(delay)
    print(f"finished.total reward: {total:.1f}")

if __name__ == "__main__":
    run()


