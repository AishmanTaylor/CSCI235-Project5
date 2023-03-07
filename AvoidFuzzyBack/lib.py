from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
import pybricks.nxtdevices

REFRESH = 2000


def executor(robot, action, condition):
    action(robot)
    while True:
        robot.loops += 1
        update = condition(robot)
        if update:
            action, condition = update
            action(robot)
        if robot.loops > REFRESH:
            robot.loops = 0
            robot.show(action, condition)


class SensorMotor:
    def __init__(self, ev3):
        self.ev3 = ev3
        self.left = Motor(Port.A)
        self.right = Motor(Port.D)        
        self.control = TouchSensor(Port.S3)
        self.left_sonar = pybricks.nxtdevices.UltrasonicSensor(Port.S1)
        self.right_sonar = pybricks.nxtdevices.UltrasonicSensor(Port.S4)
        self.front_sonar = UltrasonicSensor(Port.S2)
        self.loops = 0

    def values(self):
        return ["L:" + str(self.left_sonar.distance()), 
            "F:" + str(self.front_sonar.distance()), 
            "R:" + str(self.right_sonar.distance()),
            "C:" + str(self.control.pressed())]

    def show(self, action, condition):
        self.ev3.screen.clear()
        self.ev3.screen.draw_text(0, 0, action.__name__)
        self.ev3.screen.draw_text(0, 16, condition.__name__)
        y = 32
        for value in self.values():
            self.ev3.screen.draw_text(0, y, value)
            y += 16


def f_and(v1, v2):
    return min(v1, v2)


def f_or(v1, v2):
    return max(v1, v2)


def f_not(value):
    return 1.0 - value


def rising(value, start, end):
    if value > end:
        return 1.0
    elif value < start:
        return 0.0
    else:
        return (value - start) / (end - start)


def falling(value, start, end):
    return f_not(rising(value, start, end))


def trapezoid(value, start, peak_start, peak_end, end):
    if value <= peak_end:
        return rising(value, start, peak_start)
    else:
        return falling(value, peak_end, end)


def triangle(value, start, peak, end):
    return trapezoid(value, start, peak, peak, end)


def defuzzify(value, zero, one):
    if zero > one:
        return defuzzify(f_not(value), one, zero)
    else:
        return zero + value * (one - zero)


def empty_action(robot):
    pass


def go_forward(robot):
    robot.left.run(360)
    robot.right.run(360)

def go_back(robot):
    robot.left.run(-360)
    robot.right.run(-360)