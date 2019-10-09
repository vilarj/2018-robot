#
# See the documentation for more details on how this works
#
# The idea here is you provide a simulation object that overrides specific
# pieces of WPILib, and modifies motors/sensors accordingly depending on the
# state of the simulation. An example of this would be measuring a motor
# moving for a set period of time, and then changing a limit switch to turn
# on after that period of time. This can help you do more complex simulations
# of your robot code without too much extra effort.
#
# NOTE: THIS API IS ALPHA AND WILL MOST LIKELY CHANGE!
#       ... if you have better ideas on how to implement, submit a patch!
#

from pyfrc.physics import drivetrains

try:
    from pyfrc.physics.visionsim import VisionSim
except ImportError:
    VisionSim = None

from networktables import NetworkTables

#from components.drive import Drive


class PhysicsEngine(object):
    '''
        Simulates a motor moving something that strikes two limit switches,
        one on each end of the track. Obviously, this is not particularly
        realistic, but it's good enough to illustrate the point

    '''

    def __init__(self, physics_controller):
        '''
            :param physics_controller: `pyfrc.physics.core.PhysicsInterface` object
                                       to communicate simulation effects to
        '''

        self.physics_controller = physics_controller
        self.position = 0

        self.elevator_position = 0
        self.fork_position = 0

        self.ft_per_sec = 5
        self.wheel_circumference = 18.8

        self.physics_controller.add_device_gyro_channel('adxrs450_spi_0_angle')

    @property
    def nt(self):
        try:
            return self._nt
        except AttributeError:
            self._nt = NetworkTables.getTable('/')
            return self._nt

    def update_sim(self, hal_data, now, tm_diff):
        '''
            Called when the simulation parameters for the program need to be
            updated.

            :param now: The current time as a float
            :param tm_diff: The amount of time that has passed since the last
                            time that this function was called
        '''

        # Simulate the drivetrain
        l_motor = hal_data['CAN'][5]['value']
        r_motor = hal_data['CAN'][6]['value']

        speed, rotation = drivetrains.two_motor_drivetrain(l_motor, r_motor, speed=self.ft_per_sec)
        self.physics_controller.drive(speed, rotation, tm_diff)

        # Inches we traveled
        distance_inches = 12.0*speed*tm_diff

        # Use that to give a rough approximation of encoder values.. not
        # accurate for turns, but we don't need that
        # -> encoder = distance / (wheel_circumference / 360.0)

        #hal_data['encoder'][0]['count'] += int(distance_inches / (self.wheel_circumference/360.0))

        # Elevator simulation
        e_motor = hal_data['CAN'][7]['value']
        e_distance = e_motor * tm_diff * 2
        #print(e_distance)

        self.elevator_position = (self.elevator_position + e_distance)
        self.elevator_position = max(min(6, self.elevator_position), 0)

        hal_data['CAN'][7]['quad_position'] = int(self.elevator_position * (360 * 4))

        # When is at the botton - do this
        if 0 <= self.elevator_position < 0.1:
            hal_data['CAN'][7]['limit_switch_closed_rev'] = True
        # if it's not at the bottom - don't do this
        else:
            hal_data['CAN'][7]['limit_switch_closed_rev'] = False

        # When is at the top - do this
        if 5.9 <= self.elevator_position < 6.0:
            hal_data['CAN'][7]['limit_switch_closed_for'] = True
        # if it's not at the top - don't do this
        else:
            hal_data['CAN'][7]['limit_switch_closed_for'] = False

        # Set our limit switches
        # if 0 <= self.elevator_position < 0.2:
        #     hal_data['dio'][3]['value'] = True
        # else:
        #     hal_data['dio'][3]['value'] = False
        #
        # if 2.4 < self.elevator_position < 2.6:
        #     hal_data['dio'][2]['value'] = True
        # else:
        #     hal_data['dio'][2]['value'] = False
        #
        # if 4.9 < self.elevator_position <= 5:
        #     hal_data['dio'][1]['value'] = True
        # else:
        #     hal_data['dio'][1]['value'] = False

        # arm motor limit switches
        # -> it's on if either end is hit
        arm_motor = hal_data['CAN'][8]['value']
        self.fork_position += arm_motor * tm_diff

        self.fork_position = max(min(3, self.fork_position), 0)
        if (0 <= self.fork_position <= 0.1) or (2.9 <= self.fork_position <= 3):
            hal_data['dio'][3]['value'] = True
        else:
            hal_data['dio'][3]['value'] = False
