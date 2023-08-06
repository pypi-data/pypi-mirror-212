import Signal8

env = Signal8.env('disaster_response')
env.reset(options={"scenario_num": 0})
observation, _, terminations, truncations, _ = env.last()
entities = env.unwrapped.get_start_state()
env.step(1)
env.close()