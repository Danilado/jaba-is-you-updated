# distutils: language=c++
# cython: profile=True
from copy import copy


def copy_matrix(list matrix) -> list:
    copy_matrix = []
    for i in range(len(matrix)):
        copy_matrix.append([])
        for j in range(len(matrix[i])):
            copy_matrix[i].append([])
            for obj in matrix[i][j]:
                copy_obj = copy(obj)
                copy_matrix[i][j].append(copy_obj)
    return copy_matrix
