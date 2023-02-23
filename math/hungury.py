from scipy.optimize import linear_sum_assignment
import numpy as np
mat=\
[
[20,11,16,16,14 ],
[11,10,12,17,8 ],
[16,12,14,15,11 ],
[23,9,23,17,17 ],
[18,10,15,14,13 ],
[29,13,33,35,21 ],
[25,11,35,31,18 ],
[32,23,40,40,23 ],
]

mat1=\
[
[20,11,16,16,14,1000,1000,1000],
[11,10,12,17,8,1000,1000,1000],
[16,12,14,15,11,1000,1000,1000],
[23,9,23,17,17,1000,1000,1000],
[18,10,15,14,13,1000,1000,1000],
[29,13,33,35,21,1000,1000,1000],
[25,11,35,31,18,1000,1000,1000],
[32,23,40,40,23,1000,1000,1000],
]

mat2=\
[
[20,11,1000,16,14,1000,1000,1000],
[11,10,1000,17,8,1000,1000,1000],
[16,12,14,15,11,1000,1000,1000],
[23,9,1000,17,17,1000,1000,1000],
[18,10,15,14,13,1000,1000,1000],
[29,13,1000,35,21,1000,1000,1000],
[25,11,1000,31,18,1000,1000,1000],
[32,23,1000,40,23,1000,1000,1000],
]

mat=np.array(mat2).T
print(linear_sum_assignment(mat))




# mat=\
# [
# [20,11,16,16,14,1000,1000,1000],
# [11,10,12,17,8,1000,1000,1000],
# [16,12,14,15,11,1000,1000,1000],
# [23,9,23,17,17,1000,1000,1000],
# [18,10,15,14,13,1000,1000,1000],
# [29,13,33,35,21,1000,1000,1000],
# [25,11,35,31,18,1000,1000,1000],
# [32,23,40,40,23,1000,1000,1000],
# ]