# FAN CONTROLLER SYSTEM - PROJECT OVERVIEW

## What system is modeling?

A fan controller that automatically reacts to the environmental temperature changes by transitioning between operational states. The system prioritizes fault prevention and maintains safe operating temperatures by switching modes based on defined thresholds.

---

## Why FSM is suitable?
The fan controller's behavior depends on both current state and current input (the same temperature reading can produce different responses depending on what mode the system is already in). FSM is suitable because it eliminates redundant conditional checks and boolean flags, enforces valid state transitions, makes it easier to debug, update and maintain without breaking existing behavior

---

## What OOP concepts are used?

**Inheritance** - Each operational state (Idle, Running, Cooling, Error) inherits from a shared base `State` class, for reuse and consistent structure across states

**Polymorphism** - The fan controller invokes the same interface across all states, but each state responds differently, for instance, the same temperature input can triggers cooling in this state but can also be an error in another.

**Encapsulation** - User interactions (start, stop, reset) are intentionally limited in scope, which means internal data are protected from external modification, for example, temperature thresholds and state transition logic in this fan controller, to ensure system safety and stability.

---

## What major features exist?

**Automatic temperature-driven state transitions** - the system continuously monitors temperature and transitions states without manual control from users

**User mode controls** - users can interact (`start`, `stop`, `reset`) with the system through the controlled interface without exposing internal logic

**Fault detection and error state** - critical temperature or hardware fault locks the system into a protected error state to prevent hardware damages

**Manual reset only with safety guard** - to ensure the users acknowledges the fault before resuming normal operatio, reset will be denied if temperature is still critical


## State Transitions
 
| Temperature | Active State | Result |
|---|---|---|
| < 60C | Any | Idle |
| ≥ 60C | Idle / Running | Cooling |
| ≥ 80C | Any | Error |
| Fault = True | Any | Error (immediate) |
| Reset (temp < 60C) | Error | Idle |
| Reset (60C ≤ temp < 80C) | Error | Cooling |
| Reset (temp ≥ 80C) | Error | Denied — stays in Error |