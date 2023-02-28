import lib

CLOSE = 100
FAR = 500
SPEED = 500

# def fuzzy_condition(robot):
#     if robot.control.pressed():
#         return lib.go_forward, open_condition

#     front_close = lib.falling(robot.front_sonar.distance(), CLOSE, FAR)
#     front_far = lib.rising(robot.front_sonar.distance(), FAR, CLOSE)

#     left_wheel  = lib.defuzzify(lib.f_or(front_close, front_far), 0, -SPEED)
#     right_wheel = lib.defuzzify(lib.f_or(front_close, front_far), 0, -SPEED)

#     robot.left.run(left_wheel)
#     robot.right.run(right_wheel)


# def open_condition(robot):
#     if not robot.control.pressed():
#         return lib.empty_action, fuzzy_condition

def forward_fuzzy_condition(robot):
    front_far = lib.rising(robot.front_sonar.distance(), CLOSE, FAR)
    left_wheel  = lib.defuzzify(front_far, 0, SPEED)
    right_wheel = lib.defuzzify(front_far, 0, SPEED)
    robot.left.run(left_wheel)
    robot.right.run(right_wheel)

    if robot.front_sonar.distance() <= CLOSE:
        return lib.empty_action, backwards_fuzzy_condition

def backwards_fuzzy_condition(robot):
    front_close = lib.falling(robot.front_sonar.distance(), CLOSE, FAR)
    left_wheel  = lib.defuzzify(front_close, 0, -SPEED)
    right_wheel = lib.defuzzify(front_close, 0, -SPEED)
    robot.left.run(left_wheel)
    robot.right.run(right_wheel)

    if robot.front_sonar.distance() >= FAR:
        return lib.go_forward, forward_fuzzy_condition