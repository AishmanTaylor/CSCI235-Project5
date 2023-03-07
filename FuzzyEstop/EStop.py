import lib

CLOSE = 100
FAR = 500
SPEED = 500

# def fuzzy_condition(robot):
#     if robot.control.pressed():
#         return lib.go_forward, open_condition

#     front_close = lib.falling(robot.front_sonar.distance(), CLOSE, FAR)
#     left_close  = lib.falling(robot.left_sonar.distance(),  CLOSE, FAR)
#     right_close = lib.falling(robot.right_sonar.distance(), CLOSE, FAR)

#     left_wheel  = lib.defuzzify(lib.f_or(front_close, left_close),  0, -SPEED)
#     right_wheel = lib.defuzzify(lib.f_or(front_close, right_close), 0, -SPEED)

#     robot.left.run(left_wheel)
#     robot.right.run(right_wheel)


# def open_condition(robot):
#     if not robot.control.pressed():
#         return lib.empty_action, fuzzy_condition
forward = True

def AvoidFuzzyBack(robot):
    front_distance = robot.front_sonar.distance()
    left_distance = robot.left_sonar.distance()
    right_distance = robot.right_sonar.distance()

    front_close = lib.rising(front_distance, CLOSE, FAR)
    left_wheel_close  = lib.defuzzify(front_close,  0, -SPEED)
    right_wheel_close = lib.defuzzify(front_close, 0, -SPEED)
    left_close  = lib.rising(left_distance,  CLOSE, FAR)
    left_wheel_left  = lib.defuzzify(left_close,  0, 0)
    right_wheel_left = lib.defuzzify(left_close, 0, -SPEED)
    right_close = lib.rising(right_distance, CLOSE, FAR)
    left_wheel_right  = lib.defuzzify(right_close,  0, 0)
    right_wheel_right = lib.defuzzify(right_close, 0, -SPEED)
    
    if (front_distance >= FAR) and (right_distance >= FAR) and (left_distance >= FAR):
        forward = True
        robot.left.run(SPEED)
        robot.right.run(SPEED)
        return lib.empty_action, estop 
    elif front_distance <= FAR:
        return lib.go_back, go_back
    elif left_distance <= FAR:
        robot.left.run(left_wheel_left)
        robot.right.run(SPEED)
    elif right_distance <= FAR:
        robot.left.run(SPEED)
        robot.right.run(right_wheel_right)

def go_back(robot):
    front_distance = robot.front_sonar.distance()
    left_distance = robot.left_sonar.distance()
    right_distance = robot.right_sonar.distance()

    front_close = lib.falling(front_distance, CLOSE, FAR)
    left_wheel_close  = lib.defuzzify(front_close,  0, SPEED)
    right_wheel_close = lib.defuzzify(front_close, 0, SPEED)
    left_close  = lib.falling(left_distance,  CLOSE, FAR)
    left_wheel_left  = lib.defuzzify(left_close,  0, 0)
    right_wheel_left = lib.defuzzify(left_close, 0, SPEED)
    right_close = lib.falling(right_distance, CLOSE, FAR)
    left_wheel_right  = lib.defuzzify(right_close,  0, 0)
    right_wheel_right = lib.defuzzify(right_close, 0, SPEED)

    if front_distance <= FAR:
        forward = False
        robot.left.run(-left_wheel_close)
        robot.right.run(-right_wheel_close)
        return lib.empty_action, estop
    elif left_distance <= FAR:
        robot.left.run(-left_wheel_left)
        robot.right.run(SPEED)
    elif right_distance <= FAR:
        robot.left.run(SPEED)
        robot.right.run(-right_wheel_right)
    elif (front_distance >= FAR) and (right_distance >= FAR) and (left_distance >= FAR):
        return lib.go_forward, AvoidFuzzyBack

def estop(robot):
    if robot.control.pressed():
        return lib.empty_action, state_sink
    elif forward == True:
        return lib.empty_action, AvoidFuzzyBack
    elif forward == False:
        return lib.empty_action, go_back

def state_sink(robot):
    robot.left.run(0)
    robot.right.run(0)
    return lib.empty_action, state_sink