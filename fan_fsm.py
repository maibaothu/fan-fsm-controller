# -------------------------------------------------------------
# FAN CONTROLLER - FSM + OOP Implementation
# -------------------------------------------------------------
# Blueprint 1: Base class "State", the skeleton for all the states
class State:
    def handle(self, context):
        pass

    def name(self):
        return self.__class__.__name__

# Blueprint 2: System brain
class FanController:

    # Temperature thresholds
    TEMP_HIGH = 60
    TEMP_CRITICAL = 80

    def __init__(self):
        self.state = IdleState()
        self.temp = 25
        self.fault = False
        self.event = None

    def set_state(self, state):
        print(f"Transitioning from {self.state.name()} to {state.name()} ...")
        self.state = state

    def update(self):
        self.state.handle(self)

    def print_status(self):
        print(f"System state: {self.state.name()} | Temp: {self.temp} | Fault: {self.fault}")

    # Priority transition check 
    def priority_check(self):
        if self.fault:
            self.set_state(ErrorState())
            self.event = None
            return True
        if self.temp == self.TEMP_CRITICAL:
            self.set_state(ErrorState())
            self.event = None
            return True
        return False
    
    # User events
    def start(self):
        self.event = "start"
    
    def stop(self):
        self.event = "stop"
    
    def reset(self):
        self.event = "reset"

# Blueprint 3: Build state Idle
class IdleState(State):
    def handle(self, context):
        # Priority 1: Fault check
        if context.priority_check():
            return
        
        # Priority 2: Normal Transition
        if context.temp >= context.TEMP_CRITICAL:
            context.set_state(ErrorState())
        elif context.temp >= context.TEMP_HIGH:
            context.set_state(CoolingState())
    
        # Priority 3: User Events
        elif context.event == "start":
            context.set_state(RunningState())
        
        # Clear the event queue
        context.event = None

# Blueprint 4: Build State Running
class RunningState(State):
    def handle(self, context):
        # Priority 1: Fault check
        if context.priority_check():
            return
        
        # Priority 2: Normal Transition
        if context.temp >= context.TEMP_CRITICAL:
            context.set_state(ErrorState())
        elif context.temp >= context.TEMP_HIGH:
            context.set_state(CoolingState())
        
        # Priority 3: User Events
        elif context.event == "stop":
            context.set_state(IdleState())
        elif context.event == "start":
            print("System is already running.")
        
        # Clear the event queue
        context.event = None

# Blueprint 4: Build State Cooling
class CoolingState(State):
    def handle(self, context):
        # Priority 1: Fault check
        if context.priority_check():
            return
        
        # Priority 2: Normal Transition
        if context.temp >= context.TEMP_CRITICAL:
            context.set_state(ErrorState())
        elif context.temp < context.TEMP_HIGH:
            context.set_state(IdleState())
        
        # Priority 3: User Event
        elif context.event == "stop":
            context.set_state(IdleState())

        # Clear the event queue
        context.event = None

# Blueprint 4: Build State Error
class ErrorState(State):
    # Stay until reset (user mode)
    def handle(self, context):
        if context.event == "reset":
            context.fault = False # clear the fault
            if context.temp < context.TEMP_HIGH:
                context.set_state(IdleState())
            elif context.temp < context.TEMP_CRITICAL:
                context.set_state(CoolingState())
            else:
                print("Reset denied: temperature still critical!")
                
        # Clear the event queue
        context.event = None

# -------------------------------------------------------------
# FAN CONTROLLER - FSM + OOP Implementation
# -------------------------------------------------------------

if __name__ == "__main__":
    fan = FanController()
    print("[Test 1] Current State - Expected: 25C Idle by default:")
    fan.print_status()

    print("[Test 2] User starts the system - Expected: Running")
    fan.start()
    fan.update()
    fan.print_status()

    print("[Test 3] Temperature gets high - Expected: Cooling")
    fan.temp = 75
    fan.update()
    fan.print_status()

    print("[Test 4] Temperature reaches critical - Expected: Error")
    fan.temp = 85
    fan.update()
    fan.print_status()

    print("[Test 5] Reset while temperature still critical - Expected: denied, stays in Error")
    fan.reset()
    fan.update()
    fan.print_status()

    print("[Test 6] Temperature drops, user resets - Expected: Idle")
    fan.temp = 50
    fan.reset()
    fan.update()
    fan.print_status()

    print("[Test 7] Fault injected while running - Expected: Error")
    fan.start()
    fan.update()
    fan.fault = True
    fan.update()
    fan.print_status()

    print("[Test 8] User resets after fault - Expected: Idle, Fault clear")
    fan.reset()
    fan.update()
    fan.print_status()

    print("[Test 9] User starts then stops - Expected: Idle")
    fan.start()
    fan.update()
    fan.stop()
    fan.update()
    fan.print_status()