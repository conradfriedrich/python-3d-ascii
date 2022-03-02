# DONE write a test in here with a simple matrix to go
# DONE maybe a performance dip comes from using int and float? -- doesnt change result

# This is a failed attempt at implementing a fast arbitraty scaling operation on pygame surf_arrays.
# I thought matrix multiplication is the way to go, but it is SLOWER than using a for loop. Also only
# using one cpu core, there might be hope in multithreading, but not much. just way to slow. I wonder
# how pygame implements their caling function, which is much faster.

import numpy as np
import pygame


def main():
    print("main")
    print(pygame.transform.__file__)
    M = np.ones((480, 270, 3))
    scaler = Scaler(np.shape(M), 5)
    Q = scaler.scale(M)
    print_3d(Q)


def print_3d(array):
    print("3D Printing ")
    for i in range(np.shape(array)[2]):
        print(array[:, :, i])


class Scaler:
    def __init__(self, shape, factor=3):

        self.num_row, self.num_col, self.num_dim = shape
        self.factor = factor

        self.R = self.__right_matrix()
        self.L = self.__left_matrix()

    def scale(self, M):
        # This is done explicitly and cumbersomely because of numpys way of ordering dimensions
        # as opposed to pygames' way.
        A = np.matmul(M[:, :, 0], self.R[:, :, 0])
        A = np.matmul(self.L[:, :, 0], A)
        B = np.matmul(M[:, :, 1], self.R[:, :, 1])
        B = np.matmul(self.L[:, :, 1], B)
        C = np.matmul(M[:, :, 2], self.R[:, :, 2])
        C = np.matmul(self.L[:, :, 2], C)
        return np.stack((A, B, C), axis=2)

    def __right_matrix(self):

        eyes = []

        for i in range(0, self.factor):
            # set dtype to uint8
            eye = np.eye(self.num_col, dtype="float32")
            eyes.append(eye)

        print(len(eyes), self.num_col)
        sum_num_col = self.factor * self.num_col
        mixed_eye = np.ravel(eyes, order="F").reshape(self.num_col, sum_num_col)
        mixed_eye_3d = np.repeat(mixed_eye[:, :, np.newaxis], 3, axis=2)

        return mixed_eye_3d

    def __left_matrix(self):

        eyes = []

        for i in range(0, self.factor):
            # set dtype to uint8
            eye = np.eye(self.num_row, dtype="B")
            eyes.append(eye)

        sum_num_row = self.factor * self.num_row
        mixed_eye = np.ravel(eyes, order="F").reshape(self.num_row, sum_num_row).T
        mixed_eye_3d = np.repeat(mixed_eye[:, :, np.newaxis], 3, axis=2)

        return mixed_eye_3d


if __name__ == "__main__":
    main()
