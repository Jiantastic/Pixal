import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

placeholder = [[[99, 156, 0], [96, 159, 0], [94, 161, 0], [91, 164, 0], [82, 173, 0]], [[71, 184, 0], [23, 232, 0], [0, 246, 9], [0, 230, 25], [0, 224, 31]], [[0, 225, 30], [6, 249, 0], [37, 218, 0], [71, 184, 0], [77, 178, 0]], [[55, 200, 0], [0, 244, 11], [0, 213, 42], [0, 207, 48], [0, 201, 54]], [[0, 212, 43], [0, 230, 25], [0, 205, 50], [0, 199, 56], [0, 194, 61]]]

graphData = np.array(placeholder,dtype=np.uint8)

plt.imshow(placeholder,origin='lower')

plt.colorbar()

plt.suptitle('infrared temperature heat map',fontsize=20)

plt.show()