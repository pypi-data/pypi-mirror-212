from v3dpy.loaders.pbd import PBD
from neuron_image_denoise.filter import *


if __name__ == '__main__':
    i = PBD().load('data/flare_break.v3dpbd')
    i = gauss_attenuation_filter(i[0])
    i[i>255] = 255
    i = i.astype(np.uint8)
    PBD(pbd16_full_blood=False).save('data/out.v3dpbd', np.array([i]))
