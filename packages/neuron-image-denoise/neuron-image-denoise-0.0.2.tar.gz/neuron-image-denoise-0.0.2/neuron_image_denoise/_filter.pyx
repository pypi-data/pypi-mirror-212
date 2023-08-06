import cython
cimport cython
import numpy as np
cimport numpy as np
from libcpp.vector cimport vector


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cpdef np.ndarray[np.uint16_t, ndim=3] adaptive_denoise(np.ndarray[np.uint16_t, ndim=3] img,
                                                       tuple ada_interval, tuple flare_interval,
                                                       int ada_sampling, int flare_sampling, float flare_weight,
                                                       float atten_depth, bint flare_x, bint flare_y):

    cdef:
        int fix, fiy, fiz, aix, aiy, aiz
        long long x, y, z, i
    fiz, fiy, fix = flare_interval
    aiz, aiy, aix = ada_interval

    # prepare weights
    cdef:
        vector[float] w
    for i in range(flare_sampling):
        w.push_back(1 / ((i * fiz / atten_depth) ** 2 + 1))
    cdef float s = sum(w)
    for i in range(flare_sampling):
        w[i] *= flare_weight / s

    # filtering
    cdef:
        np.ndarray[np.uint16_t, ndim = 3] out = np.zeros_like(img)
        long long dimx = img.shape[2], dimy = img.shape[1], dimz = img.shape[0]
        float ada_sum, fx, fy
        int ada_count, sx, sy, sz
    for z in range(dimz):
        for y in range(dimy):
            for x in range(dimx):
                ada_sum = 0
                ada_count = 0
                sx = sy = sz = 0
                for i in range(ada_sampling):
                    sx += aix
                    sy += aiy
                    sz += aiz
                    if x >= sx:
                        ada_sum += img[z, y, x - sx]
                        ada_count += 1
                    if x + sx < dimx:
                        ada_sum += img[z, y, x + sx]
                        ada_count += 1
                    if y >= sy:
                        ada_sum += img[z, y - sy, x]
                        ada_count += 1
                    if y + sy < dimy:
                        ada_sum += img[z, y + sy, x]
                        ada_count += 1
                    if z >= sz:
                        ada_sum += img[z - sz, y, x]
                        ada_count += 1
                    if z + sz < dimz:
                        ada_sum += img[z + sz, y, x]
                        ada_count += 1
                fx = fy = 0
                sx = sy = sz = 0
                for i in range(flare_sampling):
                    sx += fix
                    sy += fiy
                    sz += fiz
                    if z + sz < dimz:
                        if flare_x:
                            if x >= sx:
                                pass
                            if x + sx < dimx:
                                pass
                            fx += w[i] * img[z + sz, y, x]
                        if flare_y:
                            if y >= sy:
                                pass
                            if y + sy < dimy:
                                pass
                            fy += w[i] * img[z + sz, y, x]
                out[z, y, x] = <np.uint16_t>max(img[z, y, x] - ada_sum / ada_count - max(fx, fy), 0)
    return out