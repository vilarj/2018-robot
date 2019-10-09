#import math
import wpilib

from magicbot import will_reset_to

class DriveTrain:
    '''
        Simple magicbot drive object
    '''

    #wall_p = tunable(-1.8)
    #distance = tunable(0)
    #analog = tunable(0)

    #tx = tunable(0)
    #ty = tunable(0)
    #offset = tunable(1.0)

    #MaxY = tunable(0.8)

    #ultrasonic = wpilib.AnalogInput
    drive: wpilib.drive.DifferentialDrive
    gyro: wpilib.ADXRS450_Gyro

    x = will_reset_to(0)
    y = will_reset_to(0)

    def __init__(self):
        self.moveDeg = None
        self.saveAng = None
         # This stores the information of moveDeg for the second time

# distance is .98
    def move(self, y, x):
        self.y = y
        self.x = x -0.135

    def move2(self, deg):
        self.moveDeg = deg

    def rotate(self, x):
        self.x = x

    def execute(self):
        self.tx = self.x
        self.ty = self.y

        if self.moveDeg != None:
            if self.saveAng == None:
                self.saveAng = self.gyro.getAngle()
            wantAngle = self.saveAng + self.moveDeg
            angle = self.gyro.getAngle()
            error = angle - wantAngle
            print(error)
            output = (error * 0.01)
            output = max(min(0.5, output), -0.5)
            self.x = output
            self.moveDeg = None

        self.drive.arcadeDrive(self.y, self.x, True)
