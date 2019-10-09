

from magicbot import AutonomousStateMachine, timed_state, state
import wpilib
import components.forklift
import components.drive_train
import components.fork

class DriveForward(AutonomousStateMachine):
    MODE_NAME = 'Drive Forward'
    DEFAULT = True

    # Injected from the definition in robot.py
    forklift: components.forklift.Forklift
    fork: components.fork.Fork
    driveTrain: components.drive_train.DriveTrain
    #left side

    @timed_state(duration=3.2, first=True, next_state='turning')
    def drive_forward(self, initial_call):
        self.driveTrain.move(-0.8, 0)

    @timed_state(duration=0.5, next_state='rais')
    def turning(self):
        self.driveTrain.move(0,-0.7)

    @timed_state(duration=1.2, next_state='drop')
    def rais(self):
        self.forklift.top()

    @timed_state(duration=1)
    def drop(self):
        self.fork.open()

"""
    @timed_state(duration=1, next_state='deposit')
    def deposit_powercube(self, initial_call):
        self.fork.top()
"""
    #right side
"""
@timed_state(duration=3.2, first=True, next_state='turning')
def drive_forward(self, initial_call):
        self.driveTrain.move(-0.8, 0.135)

@timed_state(duration=0.5, next_state='rais')
def turning(self):
        self.driveTrain.move(0,0.7)

@timed_state(duration=1.2, next_state='drop')
def rais(self):
        self.forklift.top()

@timed_state(duration=1)
def drop(self):
        self.fork.open()

@timed_state(duration=1, next_state='despotit')
def deposit_powercube(self, initial_call):
        self.fork.top()
"""
