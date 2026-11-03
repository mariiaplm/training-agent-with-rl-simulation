# Records one run of the trained agent and writes it out as run.js,
#a list of per timestep frames (floor, calls, destinations, action, reward)
#that index.html replays in the browser

import json
from elevator_env import ElevatorEnv
from train import load_q_table, N_FLOORS, ARRIVAL_RATE

def export_run(path = "run.js", steps = 100):

    q_table = load_q_table()
    env = ElevatorEnv(N_FLOORS, steps, ARRIVAL_RATE)
    frames = []
    state = env.reset()
    total = 0.0
    done = False

    while not done:
        values = q_table[state]
        action = values.index(max(values))
        state, reward, done, info = env.step(action)
        total += reward
        frames.append({
            "floor": env.current_floor,
            "calls": list(env.calls),
            "destination": list(env.destination),
            "action": action,
            "reward": reward,
            "total": total,
            "delivered": info["delivered"]
        })

    with open(path, "w") as f:
        f.write("const RUN = " + json.dumps(frames) + ";")


if __name__ == "__main__":
    export_run()