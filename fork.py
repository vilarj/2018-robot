

import ctre
from ctre import WPI_TalonSRX
from magicbot import AutonomousStateMachine, timed_state, state # state_tm
from magicbot import tunable, will_reset_to

import wpilib

class Fork:
    fork_switch: wpilib.DigitalInput
    arm_motor: ctre.WPI_TalonSRX

    position = will_reset_to(0)
    last_position = 0

    fork_switch_on = tunable(False)

    def execute(self):

        # TODO: the limit switch seems to be broken on the robot :(
        self.fork_switch_on = self.fork_switch.get()

        # if the limit switch is on and you last opened it,
        # and you are trying to open it
        #if self.fork_switch_on and self.position and self.last_position == self.position:
        #    self.position = 0
        #elif self.position != 0: # if nothing is being pressed - do this
        #    self.last_position = self.position

        self.arm_motor.set(self.position)
        #self.arm_motor.set(0)
    # @timed_state(state_tm)
    def open(self):
        self.position = -1

    def close(self):
        self.position = 1
