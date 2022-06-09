"""
This script contains joint connection information.
Author: Mosam Dabhi
Date: June 8, 2022
"""

import numpy as np


def get_joints(str_object):
    R = np.zeros((3, 3))
    if str_object == "Human":
        joint_connections = (
            (14, 15),
            (15, 16),
            (13, 12),
            (12, 11),
            (9, 8),
            (8, 7),
            (4, 5),
            (5, 6),
            (3, 2),
            (2, 1),
            (7, 0),
            (0, 4),
            (0, 1),
            (8, 11),
            (8, 14),
            (9, 10),
        )
        range_scale = 1

    elif str_object == "Cheetah":
        joint_connections = (
            (3, 1),
            (1, 0),
            (1, 2),
            (3, 4),
            (4, 5),
            (5, 6),
            (6, 7),
            (8, 9),
            (9, 10),
            (3, 8),
            (3, 11),
            (11, 12),
            (12, 13),
            (5, 17),
            (17, 18),
            (18, 19),
            (5, 14),
            (14, 15),
            (15, 16),
            (4, 14),
            (4, 17),
        )
        range_scale = 1

    elif str_object == "Flamingo":
        joint_connections = (
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 4),
            (4, 5),
            (5, 6),
            (3, 6),
            (6, 7),
            (7, 8),
            (6, 9),
            (9, 10),
        )
        range_scale = 1

    elif str_object == "Tiger":
        joint_connections = (
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 4),
            (2, 5),
            (5, 6),
            (2, 7),
            (7, 8),
            (8, 9),
            (9, 10),
            (8, 11),
            (11, 12),
            (8, 13),
            (13, 14),
            (14, 15),
        )
        range_scale = 1

    elif str_object == "Fish":
        joint_connections = (
            (0, 1),
            (1, 2),
            (2, 3),
            (1, 3),
            (3, 4),
            (4, 5),
            (5, 6),
            (6, 7),
            (5, 7),
            (5, 8),
            (8, 9),
            (9, 10),
            (8, 10),
            (10, 11),
            (11, 0),
        )
        range_scale = 2
        R[0, 0], R[0, 1], R[0, 2] = 1, 0, 0
        R[1, 0], R[1, 1], R[1, 2] = 0, 0, 1
        R[2, 0], R[2, 1], R[2, 2] = 0, 1, 0

    elif str_object == "Colobus_Monkey":
        joint_connections = (
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 4),
            (1, 5),
            (5, 6),
            (6, 7),
            (1, 8),
            (8, 9),
            (9, 10),
            (10, 11),
            (11, 12),
            (9, 13),
            (13, 14),
            (14, 15),
        )
        range_scale = 1
        R[0, 0], R[0, 1], R[0, 2] = 0, 0, 1
        R[1, 0], R[1, 1], R[1, 2] = 1, 0, 0
        R[2, 0], R[2, 1], R[2, 2] = 0, 1, 0

    elif str_object == "Chimpanzee":
        joint_connections = (
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 4),
            (1, 5),
            (5, 6),
            (6, 7),
            (1, 8),
            (8, 9),
            (9, 10),
            (10, 11),
            (11, 12),
            (9, 13),
            (13, 14),
            (14, 15),
        )
        range_scale = 1
        R[0, 0], R[0, 1], R[0, 2] = 0, 1, 0
        R[1, 0], R[1, 1], R[1, 2] = 0, 0, 1
        R[2, 0], R[2, 1], R[2, 2] = 1, 0, 0

    elif str_object == "Fly":
        joint_connections = (
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 4),
            (5, 6),
            (6, 7),
            (7, 8),
            (8, 9),
            (10, 11),
            (11, 12),
            (12, 13),
            (13, 14),
            (16, 17),
            (17, 18),
            (19, 20),
            (20, 21),
            (21, 22),
            (22, 23),
            (24, 25),
            (25, 26),
            (26, 27),
            (27, 28),
            (29, 30),
            (31, 32),
            (32, 33),
            (35, 36),
            (36, 37),
        )

    return joint_connections, range_scale, R


def extract_bone_connections(W, joint_connections):
    xlines, ylines = [], []
    for line in joint_connections:
        for point in line:
            xlines.append(W[point, 0])
            ylines.append(W[point, 1])
        xlines.append(None)
        ylines.append(None)

    return xlines, ylines
