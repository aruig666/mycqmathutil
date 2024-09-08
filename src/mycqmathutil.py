import math


def get_gear_pitch_diameter_by_shape(shape):
    '''
    :param shape: 齿形
    :return: 节圆
    '''
    if shape == "S3M":
        return 0.76
    else:
        return 0.0


def get_gear_tooth_depth_by_shape(shape):
    '''
    :param shape: 齿形
    :return: 节圆
    '''
    if shape == "S3M":
        return 1.11
    else:
        return 0.0


def solve_quadratic_equation(a, b, c):
    """
    获取一元二次方程 ax^2+bx+c=0 的实数根，重根只返回一个

    :param a: 二次项系数
    :param b: 一次项系数
    :param c: 常数项
    :return: float数组
    """
    if abs(b * b - 4 * a * c) > 0.001:
        delta = b * b - 4 * a * c

    else:
        delta = 0
    print("delta : " + str(delta))
    if delta > 0:
        return [(-b + delta ** 0.5) / (2 * a), ((-b - delta ** 0.5) / (2 * a))]
    elif delta == 0:
        return [(-b + delta ** 0.5) / (2 * a)]
    else:
        return None


def get_gear_tooth_points_and_radius_by_shape(shape, diameter, pitch_diameter, tooth_depth):
    r0 = diameter / 2 - tooth_depth
    x0 = 0
    y0 = 0

    r1 = 0.15
    r2 = 1.975
    r3 = 0.28

    x2 = 0.975
    y2 = math.sqrt((pitch_diameter / 2) ** 2 - x2 ** 2)
    n1 = ((diameter / 2 - tooth_depth + r1) ** 2 + x2 ** 2 + y2 ** 2 - (r2 - r1) ** 2) / (2 * x2)
    _y1 = solve_quadratic_equation((y2 / x2) ** 2 + 1, -2 * n1 * y2 / x2,
                                   n1 ** 2 - (diameter / 2 - tooth_depth + r1) ** 2)
    y1 = None
    for i in range(len(_y1)):
        _x1 = -y2 / x2 * _y1[i] + n1
        if _x1 < 0:
            y1 = _y1[i]
    x1 = -y2 / x2 * y1 + n1
    n3 = ((diameter / 2 - r3) ** 2 + x2 ** 2 + y2 ** 2 - (r2 + r3) ** 2) / (2 * x2)
    _y3 = solve_quadratic_equation((y2 / x2) ** 2 + 1, -2 * n3 * y2 / x2,
                                   n3 ** 2 - (diameter / 2 - r3) ** 2)
    y3 = None
    for i in range(len(_y3)):
        _x3 = -y2 / x2 * _y3[i] + n3
        if _x3 < 0:
            y3 = _y3[i]
    x3 = -y2 / x2 * y3 + n3
    point1 = get_ptoc_tangent_point(x1, y1, x0, y0, r0)
    point2 = get_ptoc_tangent_point(x1, y1, x2, y2, r2)
    point3 = get_ptoc_tangent_point(x3, y3, x2, y2, r2)
    point4 = get_ptoc_tangent_point(x3, y3, x0, y0, r0 + tooth_depth)
    return point1, r0, point2, r1, point3, r2, point4, r3


def get_ptoc_tangent_point(tx, ty, ox, oy, r):
    """
    求目标点(tx,ty)对圆(ox,oy)作相切圆后的切点。目标点如在圆内，作内切圆；如在圆外，作外切圆。

    :param tx: 目标点横坐标
    :param ty: 目标点纵坐标
    :param ox: 圆心横坐标
    :param oy: 圆心纵坐标
    :param r: 圆(ox,oy)半径
    :return: 切点[x1, y1]
    """
    distance = math.sqrt((tx - ox) ** 2 + (ty - oy) ** 2)
    # print('distance', distance)
    if distance > r:
        print("输入的数值在范围外 : " + str(distance))
        r2 = distance - r
        x1 = (tx - ox) / distance * r + ox  # 切点横坐标
        y1 = (ty - oy) / distance * r + oy  # 切点纵坐标
        return [x1, y1]
    r2 = r - distance  # 圆内所作内切圆的半径
    x1 = (tx - ox) / distance * r + ox  # 切点横坐标
    y1 = (ty - oy) / distance * r + oy  # 切点纵坐标
    return [x1, y1]
