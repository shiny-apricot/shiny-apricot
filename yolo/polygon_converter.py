import numpy as np


entry_polygon=[ [235,93], [419,250], [884,225], [562, 68] ]
exit_polygon=[ [524,647], [419,250], [884,225], [1228,598] ]

current_width=1280
current_height=720

# convert list between 0-1
def convert_to_01(polygon):
    polygon = np.array(polygon, dtype=np.float32)
    polygon[:,0] = polygon[:,0] / current_width
    polygon[:,1] = polygon[:,1] / current_height
    # take only 2 decimal point
    polygon = np.round(polygon, 2)
    # print in 1 line
    polygon = polygon.tolist()
    # take only 2 decimal point of list elements
    polygon = [ [round(x,2), round(y,2)] for x,y in polygon ]
    print(polygon)
    return polygon

convert_to_01(entry_polygon)
convert_to_01(exit_polygon)