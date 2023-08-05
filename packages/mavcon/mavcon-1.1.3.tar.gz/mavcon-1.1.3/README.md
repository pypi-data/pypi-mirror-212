# MAVCOM

### Mavlink Communicator

Provides a simplified python interface for controlling Mavlink capable flight controllers.

## Installation

```pip install mavcon```

## Basic Usage

This is an example of how to use Mavcon with a simulated vehicle.

Run SITL:

```sim_vehicle.py -v ArduCopter```

```python
from mavcon import mavcontrol
import time

vehicle = mavcon.Mavcon(
    connection_path = "127.0.0.1:14551",
)

vehicle.start()

while not vehicle.ready:
    print("Waiting for vehicle to initialise...")
    time.sleep(1)

vehicle.motors_armed = True
while not vehicle.motors_armed:
    print("Waiting for motors to spin up...")
    time.sleep(1)
    
vehicle.flight_mode = "GUIDED"
vehicle.takeoff(alt=10)
```