import lib
from pybricks.parameters import Color 

CLOSE = 100
FAR = 500
SPEED = 360

# front_distance = robot.front_sonar.distance()
# left_distance = robot.left_sonar.distance()
# right_distance = robot.right_sonar.distance()

# front_close = lib.falling(front_distance, CLOSE, FAR)
# left_wheel_close  = lib.defuzzify(front_close,  0, SPEED)
# right_wheel_close = lib.defuzzify(front_close, 0, SPEED)

# def patrol(robot):
#     if robot.light.color() == Color.WHITE:
#         return lib.go_forward, patrol
#     elif robot.light.color() != Color.WHITE:
#         return lib.go_right, reset
#     elif lib.too_close(robot) or lib.left_buttonPressed(robot) or lib.right_buttonPressed(robot):
#         return lib.go_left, sonar_check

# def sonar_check(robot):
#     if lib.too_close(robot):
#         return lib.go_left, sonar_check
#     return lib.go_forward, patrol

# def reset(robot):
#     distance_turned  = robot.left.angle()
#     if distance_turned == (460):
#         return lib.reset_angle, patrol

def patrol(robot):
    if (robot.color_sensor.color() == Color.WHITE) and (robot.front_sonar.distance() < FAR):
        return lib.go_forward, sonar_check
    elif (robot.color_sensor.color() != Color.WHITE) and (robot.front_sonar.distance() < FAR):
        return lib.go_left, reset
    elif robot.front_sonar.distance() <= FAR:
        return lib.empty_action, sonar_check

def sonar_check(robot):
    front_distance = robot.front_sonar.distance()

    front_close = lib.rising(front_distance, FAR, CLOSE)
    left_wheel_close  = lib.defuzzify(front_close,  0, SPEED)
    right_wheel_close = lib.defuzzify(front_close, 0, SPEED)

    if robot.front_sonar.distance() <= FAR:
        robot.left.run(left_wheel_close)
        robot.right.run(SPEED)
    elif robot.front_sonar.distance() >= FAR: 
        return lib.go_forward, patrol


def reset(robot):
    color_sensor = robot.color_sensor.color()
    if color_sensor != Color.WHITE:
        return lib.go_left, reset
    elif color_sensor == Color.WHITE:
        return lib.go_forward, patrol