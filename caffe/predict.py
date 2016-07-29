
import numpy as np
import sys
import caffe

caffe.set_mode_cpu()
model_def = 'deploy.prototxt'
model_weights = 'lstm.caffemodel'

net = caffe.Net(model_def,      # defines the structure of the model
                model_weights,  # contains the trained weights
                caffe.TEST)     # use test mode (e.g., don't perform dropout)