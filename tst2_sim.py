"""
A simple test of SimPy with a simple process..
"""

import simpy

# Define your base unit (e.g., 1 time unit = 1 second)
SECOND = 1
MINUTE = 60 * SECOND
HOUR = 60 * MINUTE

def patient(env):
    print(f"Patient arrived at {env.now}")
    # Clear visual meaning: wait for 15 minutes
    yield env.timeout(15 * MINUTE) 
    print(f"Patient saw doctor at {env.now}")

env = simpy.Environment()
env.process(patient(env))
env.run()
