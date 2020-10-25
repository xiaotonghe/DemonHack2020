#!/usr/bin/env python
# coding: utf-8
import matplotlib.pyplot as plt
import numpy as np
import pickle
import math
from shapely.geometry import Polygon

with open('DOMMatrix', 'rb') as f:
    # dump information to that file
    DOMMatrix = pickle.load(f)

DOMMatrix = [[float(cord) for cord in DOMMatrixEle]
             for DOMMatrixEle in DOMMatrix]


def countWithinBox(x, y, boxes):
    count = 0
    for box in boxes:
        if x > box[3] and x < box[1] and y > box[0] and y < box[2]:
            count += 1
    return count


dim = (190, 120)
matrix = np.zeros((dim[0], dim[1]))
for x in range(0, dim[0]*10, 10):
    for y in range(0, dim[1]*10, 10):
        xindex = int(x/10)
        yindex = int(y/10)
        matrix[xindex, yindex] = countWithinBox(x, y, DOMMatrix)


def getGravityVec(x, y, boxes):
    gravityLength = 200
    radSumVec = []
    for i, radius in enumerate([0, 90, 180, -90]):
        radSum = 0
        for j, length in enumerate(range(0, gravityLength, 50)):
            r = length
            Cx = x - r * math.cos(math.radians(radius))
            Cy = y - r * math.sin(math.radians(radius))
            radSum += countWithinBox(Cx, Cy, boxes) * \
                (1/(j+1))  # weighted by radius
        radSumVec.append(radSum)
    # left,top,right,bottom
    return radSumVec[2]-radSumVec[0], radSumVec[3]-radSumVec[1]


print(getGravityVec(900, 300, DOMMatrix))
