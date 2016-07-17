
import h5py
import numpy as np

h5_fn = "test.h5"

with h5py.File(h5_fn, 'w') as f:
    f['label'] = np.array([1,1,1])
    f['data'] = np.array([1,1,1])
    f['clip_markers'] = np.array([1,1,1])
