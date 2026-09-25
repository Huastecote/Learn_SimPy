"""
requires:
    pip install simpy
Summary:
    env.now = The current simulation time.
"""
import simpy


def customer(env, name, service_desk, arrival_time, service_time):
    """A customer arrives, waits for the desk, receives service, and leaves."""

    print(f" >> ENTERING customer...{name}")

    # 1. Wait until this customer's scheduled arrival time.
    yield env.timeout(arrival_time)

    print(f"{env.now:>2}: {name} arrives")

    # 2. Request the one available service desk.
    #    If another customer is using it, this process waits in line.
    #   The with statement in Python is a Context Manager. Its sole job is to guarantee cleanup (setup at the start, and cleanup at the exit).
    #   In SimPy, it automates the releasing of resources.
    #   If you don't use "with" you will need to manually: service_desk.release(request)    # Manually give the key back! 

    with service_desk.request() as request:
        yield request

        print(f"{env.now:>2}: {name} begins service")

        # 3. Simulate the service duration.
        yield env.timeout(service_time)

        print(f"{env.now:>2}: {name} departs")


def main():
    # The environment manages simulated time.
    env = simpy.Environment()

    # One service desk means only one customer can be served at a time.
    service_desk = simpy.Resource(env, capacity=1)

    print("----------The following DOES NOTTHING!!!! because customer() is a Generator!!!!")
    customer(env, "Customer A", service_desk, arrival_time=12, service_time=4)

    # Start three independent customer processes.
    print("----------Adding Customer processes...???")
    env.process(customer(env, "Customer A", service_desk, arrival_time=12, service_time=4))
    env.process(customer(env, "Customer B", service_desk, arrival_time=8, service_time=15))
    env.process(customer(env, "Customer C", service_desk, arrival_time=5, service_time=10))

    # Run until no scheduled events remain.
    print("----------Starting simulation ......")
    env.run()


if __name__ == "__main__":
    main()