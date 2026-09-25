"""
Yes, absolutely. You can dynamically create and launch new processes at any point while a SimPy simulation is actively running.
In fact, creating processes programmatically after the simulation starts is the standard way to model systems with random arrivals, 
like customers walking into a bank, web requests hitting a server, or parts arriving on a factory conveyor belt.

How to do it: The "Generator Process" Pattern
The most common way to do this is to create a master "generator" process that loops infinitely, waits for a random arrival interval, 
and then calls env.process() to spawn a new process.
Here is a clean, minimal example showing how a single factory line process spawns separate order processes over time:

"""
import simpy
import random

def order_processor(env, order_id):
    """This process is created dynamically during the simulation."""
    print(f"  [Time {env.now}]: order_processor started for Order #{order_id}")
    yield env.timeout(10)  # Simulate processing time
    print(f"  [Time {env.now}]: Order #{order_id} is complete!")

def order_generator(env):
    """This process runs the entire time and programmatically spawns new processes."""
    order_id = 1
    while True:
        # Wait a random amount of time before the next order arrives (e.g., 1 to 5 minutes)
        arrival_interval = random.randint(1, 5)
        yield env.timeout(arrival_interval)
        
        print(f"[*] New order received! Spawning a new process for Order #{order_id}...")
        
        # --- PROGRAMMATIC PROCESS CREATION ---
        # We call env.process() right here, while the simulation is running!
        env.process(order_processor(env, order_id))
        
        order_id += 1

# --- Setup ---
env = simpy.Environment()

# We only kick off the generator process initially
env.process(order_generator(env))

# Run the simulation for 20 time units
env.run(until=20)
