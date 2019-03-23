import navigator.detection_n_orientation as detection_n_orientation
import navigator.movemenets_computer as movemenets_computer
import numpy as np

# TODO: extract constants to somewhere...
# TODO: metrics?

THRESHOLD_COVERAGE= 0.050
THRESHOLD_ANGLE = 5

MOVE_AXIS_0 = 'MOVE_AXIS_0'
MOVE_AXIS_1 = 'MOVE_AXIS_1'
MOVE_AXIS_2 = 'MOVE_AXIS_2'
MOVE_BODY = 'MOVE_BODY'
MOVE_CLAW = 'MOVE_CLAW'
FORWARD_DISTANCE = 10 #e.g. cm

# Calculate what part of the image the cigarette covers.
def calculate_coverage(mask):
    return mask.reshape(-1).sum() / len(mask.reshape(-1))


# Returns a command for Wall-E in the format
# COMMAND, ARGS FOR COMMAND, CENTER_POINT
# where CENTER_POINT is the center of the object
def move(mask):
    if mask is None:
        # Wall-E hasn't discovered a cigarrette.
        return MOVE_BODY, FORWARD_DISTANCE

    degrees, center_point = detection_n_orientation.calculate_center_angle(mask)
    image_shape = mask.shape

    vertical_direction, horizontal_direction = movemenets_computer.navigation_step(image_shape, center_point)
    coverage = calculate_coverage(mask)
    if coverage <= THRESHOLD_COVERAGE:
        # In this case we have to move the CLAW!
        return MOVE_AXIS_0, horizontal_direction, MOVE_AXIS_1, vertical_direction

    if degrees > THRESHOLD_ANGLE and degrees < 180 - THRESHOLD_ANGLE:
        return MOVE_AXIS_2

    return MOVE_CLAW
