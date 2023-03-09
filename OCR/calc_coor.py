import math

def get_dist_ang(point1, point2):
    """
    Calculate both distance and angle
    Takes tuple
    point2 in this funct is hardcoded (figured out by hand (see function below)), the result can then be used 
    as a reference for any point1 in get_second_point function below it.
    """
    y_diff = point2[1] - point1[1]
    x_diff = point2[0] - point1[0]
    angle = math.atan(y_diff / x_diff)

    # Convert angle to degrees and print result
    angle_degrees = math.degrees(angle) * 100 // 1 / 100 # this fucker is to only get 2 numbers after decimal
    # print("Angle between points: {:.2f} degrees".format(angle_degrees))

    # Calculate distance between the points and print result
    distance = math.sqrt((x_diff)**2 + (y_diff)**2) * 100 // 1 / 100
    # print("Distance between points: {:.2f}".format(distance))
    return distance, angle_degrees

def get_second_point(point1, dist, ang):
    # Coordinates of the first point
    x1 = point1[0]
    y1 = point1[1]

    # Distance and angle to the second point
    d = dist
    theta_degrees = ang

    # Convert angle to radians
    theta = math.radians(theta_degrees)

    # Calculate x-coordinate of second point
    x2 = x1 + d * math.cos(theta)
    if x2 % 1 >= 0.5:
        x2 = math.ceil(x2)
    else:
        x2 = math.floor(x2)

    y2 = y1 + d * math.sin(theta)
    if y2 % 1 >= 0.5:
        y2 = math.ceil(y2)
    else:
        y2 = math.floor(y2)

    return x2, y2

def get_relative_dist_ang():
    """
    This fuckery of seemingly random numbers comes from hand calculation using my own ID as reference
    """
    coordinates = [
        [(241, 102), (657, 137)], # NIK
        [(262, 162), (663, 187)], # Name
        [(262, 190), (637, 212)], # TTL
        [(263, 218), (455, 238)], # Gender
        [(628, 224), (650, 243)], # GolDar
        [(262, 244), (660, 270)], # Alamat
        [(262, 276), (360, 297)], # RT/RW
        [(262, 302), (641, 324)], # Kel/Desa
        [(262, 331), (639, 352)], # Kecamatan
        [(262, 358), (633, 384)], # Agama
        [(262, 384), (528, 409)], # Status Kawin
        [(262, 415), (647, 434)], # Pekerjaan
        [(262, 440), (324, 464)] # WNA WNI
    ]
    res = []
    point1 = (30, 98)
    for section in coordinates:
        sek = []
        for coor in section:
            point2 = coor
            dist, ang = get_dist_ang(point1, point2)
            sek.append((dist, ang))
        res.append(sek)
    
    return res
    
# point1 = (26,468)
# point1 = (30,98)
# point2 = (262, 162)
# dist, ang = get_dist_ang(point1, point2)
# x, y = get_second_point(point1, dist, ang)
# print(x, y)