import numpy as np


def flipy(y):
    """Small hack to convert chipmunk physics to pg coordinates"""
    return -y + 600


def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm
