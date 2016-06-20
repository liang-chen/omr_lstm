
from monodata import mono

m = mono(1,1)
X, Y , testX, testY = m.load_data()

print X.shape, Y.shape, testX.shape, testY.shape
