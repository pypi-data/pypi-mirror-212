import Signal8
import time

env = Signal8.env('disaster_response')
env.reset(options={"instance_num": 0})
observation, _, terminations, truncations, _ = env.last()
time.sleep(5)
entities = env.unwrapped.get_start_state()
env.step(1)
env.close()