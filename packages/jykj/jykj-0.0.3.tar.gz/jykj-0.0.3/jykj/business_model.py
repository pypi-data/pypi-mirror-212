import cv2
import sys
import numpy as np
from typing import Union


reading_list = [[0, 0.5],
                [0.5, 1], 
                [1, 1.5],
                [1.5, 2],
                [2, 2.5]]
scale_list = ["0", "0.5", "1", "1.5", "2", "2.5"]
index_buffer = {"0": [], "0.5": [], "1": [], "1.5": [], "2": [], "2.5": []} # 每半秒更新一下识别模型检测的数字，用这个buffer预防识别模型的抖动


def rela_to_abs(coords: list, resolution: list) -> np.array:
    '''
    相对坐标转换为绝对坐标。

    参数:
        coords (list): [center_x, center_y, width, height]

        resolution (list):  [width, height]
    
    返回:
        Union[np.array, list]: 绝对坐标
    '''
    coords = np.array(coords)
    if coords.dtype == float:
        w, h = resolution
        coords[:, ::2] *= w
        coords[:, 1::2] *= h
    return coords.astype(int).tolist()


def pnpoly(verts: list, testx: int, testy: int) -> bool:
    '''
    判断点是否在多边形内部, PNPoly算法。

    参数:
        verts (list): 由多边形顶点组成的列表, 例如[[129,89],[342,68],[397,206],[340,373],[87,268]]

        testx (int): 点的x坐标, 例如123

        testy (int): 点的y坐标, 例如234

    返回:
        True: 点在多边形内

        False: 点不在多边形内
    '''

    vertx = [xyvert[0] for xyvert in verts]
    verty = [xyvert[1] for xyvert in verts]
    nvert = len(verts)
    c = False
    j = nvert - 1
    for i in range(nvert):
        if ((verty[i] > testy) !=
            (verty[j] > testy)) and (testx < (vertx[j] - vertx[i]) *
                                     (testy - verty[i]) /
                                     (verty[j] - verty[i]) + vertx[i]):
            c = not c
        j = i
    return c


def persons_in_areas(persons_coords: list,
                     areas: list,
                     resolution: list = [],
                     h_offset: float = 0,
                     w_thresh: float = -1,
                     h_thresh: float = -1) -> bool:
    '''
    判断人是否在区域内, 支持单人坐标和多人坐标, 支持单区域和多区域, 支持过滤人检测框的宽度和高度, 支持人的位置偏移。
    坐标可以使用相对坐标或绝对坐标, 人和区域的坐标类型不一致时必须指定分辨率。使用过滤高度、宽度功能且人使用绝对坐标时须指定分辨率。

    参数:
        persons_coords (list): 单人[cx, cy, w, h], 多人[[cx1, cy1, w1, h1],[cx2, cy2, w2, h2],...]

        area (list): 单区域[[x1, y1], [x2, y2], [x3, y3]], 多区域[[[x1, y1], [x2, y2], [x3, y3]], [[x4, y4], [x5, y5], [x6, y6], [x7, 7]], ...]

        resolution (list): 视频分辨率, [width, height] 

        h_offset (float): 人的位置纵向偏移量, -0.5 <= h_thresh <= 0.5

        w_thresh (float): 检测框宽度过滤阈值, 0 <= w_thresh <= 1

        h_thresh (flost): 检测框高度过滤阈值, 0 <= h_thresh <= 1

    返回:
        True: 有人在区域内

        False: 无人在区域内
    '''

    # 全部转换为多人和多区域
    assert np.array(persons_coords).ndim in [1, 2]
    assert np.array(areas).ndim in [2, 3]
    if np.array(persons_coords).ndim == 1:
        persons_coords = [persons_coords]
    if np.array(areas).ndim == 2:
        areas = [areas]

    assert -0.5 <= h_offset <= 0.5

    # 判断是相对坐标还是绝对坐标(不严格)
    abs_person = True if np.array(persons_coords).dtype == int else False
    abs_area = True if np.array(areas[0]).dtype == int else False

    if abs_person != abs_area and not resolution:
        raise ValueError("未指定视频分辨率")

    # 如果坐标类型不一致就全部转为绝对坐标
    if abs_person == True and abs_area == False:
        for area in areas:
            area = rela_to_abs(area, resolution)
    elif abs_person == False and abs_area == True:
        persons_coords = rela_to_abs(persons_coords, resolution)

    # 宽度过滤
    if w_thresh != -1:
        assert 0 < w_thresh <= 1
        if abs_person:
            if not resolution:
                raise ValueError("未指定视频分辨率")
            else:
                w_thresh = int(w_thresh * resolution[0])
        persons_coords = [p for p in persons_coords if p[2] <= w_thresh]

    # 高度过滤
    if h_thresh != -1:
        assert 0 < h_thresh <= 1
        if abs_person:
            if not resolution:
                raise ValueError("未指定视频分辨率")
            else:
                h_thresh = int(h_thresh * resolution[1])
        persons_coords = [p for p in persons_coords if p[3] <= h_thresh]

    for p in persons_coords:
        cx = p[0]
        cy = p[1] + int(h_offset * p[3])
        for area in areas:
            if pnpoly(area, cx, cy):
                return True
    return False


def compute_polygon_area(x: list, y: list) -> float:
    '''
    计算多边形面积

    参数：
        x(list):[x1,x2,...,xn]
        y(list):[y1,y2,...,yn]

    返回：
        float :多边形面积

    '''

    point_num = len(x)
    if (point_num < 3): return 0.0

    s = y[0] * (x[point_num - 1] - x[1])
    for i in range(1, point_num):
        s += y[i] * (x[i - 1] - x[(i + 1) % point_num])
    return abs(s / 2.0)


def mean_fliter(x: list, y: list, step: int) -> tuple(list, list):
    '''
    自定义均值滤波：将数据滤波，然后按等间隔提取坐标值（中值滤波同时减少数据量，减少计算时间，提高效率）

    参数：
        x(list):[x1,x2,...,xn]

        y(list):[y1,y2,...,yn]

        step(int): n
    返回：
        #滤波和筛选后的坐标值

        x(list):[x1,x2,...,xn]

        y(list):[y1,y2,...,yn]
    '''
    result_x = np.array(x)
    result_y = np.array(y)

    column = step
    rank = int(np.size(result_x) / column)

    result_x = np.resize(result_x, (rank, column))
    result_y = np.resize(result_y, (rank, column))

    result_x = np.mean(result_x, axis=1)
    result_y = np.mean(result_y, axis=1)

    return result_x.tolist(), result_y.tolist()


def mid_filter(x: list, y: list, step: int) -> tuple(list, list):
    '''
    自定义中值滤波：将数据滤波，然后按等间隔提取坐标值（中值滤波同时减少数据量，减少计算时间，提高效率）

    参数：
        x(list):[x1,x2,...,xn]

        y(list):[y1,y2,...,yn]

        step(int): n
    返回：
        #滤波和筛选后的坐标值

        x(list):[x1,x2,...,xn]

        y(list):[y1,y2,...,yn]
    '''
    result_x = np.array(x)
    result_y = np.array(y)

    column = step
    rank = int(np.size(result_x) / column)

    result_x = np.resize(result_x, (rank, column))
    result_y = np.resize(result_y, (rank, column))

    result_x = np.median(result_x, axis=1)
    result_y = np.median(result_y, axis=1)

    return result_x.tolist(), result_y.tolist()


def get_scan_area(basis_x: list, basis_y: list, cur_x: list, cur_y: list,
                  step: int) -> float:
    '''
    计算当坐标和基础坐标构成多边形面积

    参数：
        basis_x(list):基础x坐标[x1,x2,x3,.....,xn]

        basis_y(list):基础y坐标[y1,y2,y3,.....,yn]

        cur_x(list): 当前x坐标[x1,x2,x3,.....,xn]

        cur_y(list): 当前y坐标[y1,y2,y3,.....,yn]
    返回：
        result(float):两次激光点云构成多边形的面积
    '''
    basis_x, basis_y = mean_fliter(basis_x, basis_y, step=step)
    basis_x = list(reversed(basis_x))
    basis_y = list(reversed(basis_y))

    cur_x, cur_y = mean_fliter(cur_x, cur_y, step)
    cur_x += basis_x
    cur_y += basis_y
    return compute_polygon_area(cur_x, cur_y)


def get_IOU(gt_box: Union(list, tuple), b_box: Union(list, tuple)) -> float:
    '''
        计算两个矩形区域的IOU

        参数：
            gt_box (list) : 真实区域坐标 [100,100,500,500] ,shape: [1,4]

            b_box (list) : 目标区域坐标 [150,150,400,400] ,shape: [1,4]

        返回：
            两个框的重叠程度(IOU)
    '''
    assert len(gt_box) == 4 and len(b_box) == 4, '请输入正确的坐标'
    gt_box = [int(i) for i in gt_box]
    b_box = [int(i) for i in b_box]

    width0 = gt_box[2] - gt_box[0]
    height0 = gt_box[3] - gt_box[1]
    width1 = b_box[2] - b_box[0]
    height1 = b_box[3] - b_box[1]
    max_x = max(gt_box[2], b_box[2])
    min_x = min(gt_box[0], b_box[0])
    width = width0 + width1 - (max_x - min_x)
    max_y = max(gt_box[3], b_box[3])
    min_y = min(gt_box[1], b_box[1])
    height = height0 + height1 - (max_y - min_y)

    interArea = width * height
    boxAArea = width0 * height0
    boxBArea = width1 * height1
    iou = interArea / (boxAArea + boxBArea - interArea)

    return iou


def compute_density(target_area: Union(list, tuple),
                    coords: Union(list, tuple)) -> tuple(int, float):
    '''
        输入一个目标区域，一组目标坐标，计算目标数量、密度

        参数：
            target_area (list) : [[129,89],[342,68],[397,206],[340,373],[87,268]] ,shape : [n,2]

            coords (list) : [[[左上x，左上y],[右下x,右下y]]]   [[[0,0],[500,500]],[[700,700],[400,400]], [[0,0],[100,100]],[[200,200],[300,300]]] ,shape : [3,n,2]

        返回：
            return (int、float) : 目标在区域中的数量、密度
    '''
    assert len(coords) != 0, '目标数量不能为0'
    assert np.array(target_area).shape[0] > 2, '区域坐标不能少于2'
    assert len(np.array(coords).shape) >= 3, '请输入正确目标坐标'
    assert np.array(coords).shape[1] >= 2 and np.array(
        coords).shape[2] == 2, '请输入正确区域坐标'
    number = len(coords)
    if type(coords) == list:
        coords = np.array(coords)
    minx = np.min(coords[:, :, 0])
    miny = np.min(coords[:, :, 1])
    maxx = np.max(coords[:, :, 0])
    maxy = np.max(coords[:, :, 1])
    p1, p2 = ((minx, miny, maxx, maxy)), (target_area[0][0], target_area[0][1],
                                          target_area[2][0], target_area[2][1])
    iou = get_IOU(p1, p2)
    # print(iou)
    density = iou / number
    return number, float(density)


def __sst(y_no_fitting: list) -> float:
    '''
        计算SST(total sum of squares) 总平方和

        参数：

           y_no_predicted: 待拟合的y

        返回：

           总平方和SST
    '''
    y_mean = sum(y_no_fitting) / len(y_no_fitting)
    s_list =[(y - y_mean)**2 for y in y_no_fitting]
    sst = sum(s_list)
    return sst


def __ssr(y_fitting: list, y_no_fitting: list) -> float:
    '''
        计算SSR(regression sum of squares) 回归平方和

        参数：

            y_fitting: 拟合好的y值

            y_no_fitting: 待拟合y值

        返回:

            回归平方和SSR
    '''
    y_mean = sum(y_no_fitting) / len(y_no_fitting)
    s_list =[(y - y_mean)**2 for y in y_fitting]
    ssr = sum(s_list)
    return ssr


def __sse(y_fitting: list, y_no_fitting: list) -> float:
    '''
        计算SSE(error sum of squares) 残差平方和

        参数：

            y_fitting:  拟合好的y值

            y_no_fitting: 待拟合y值

        返回：

            残差平方和SSE
    '''
    s_list = [(y_fitting[i] - y_no_fitting[i])**2 for i in range(len(y_fitting))]
    sse = sum(s_list)
    return sse


def goodness_of_fit(y_fitting: list, y_no_fitting: list) -> float:
    '''
        计算拟合优度R^2
        
        参数：

             y_fitting: 拟合好的y值

             y_no_fitting: 待拟合y值

        返回:

            拟合优度R^2
    '''
    SSR = __ssr(y_fitting, y_no_fitting)
    SST = __sst(y_no_fitting)
    rr = SSR /SST
    return rr


def fit_line(x_: list,y_: list) -> tuple(float, float):
    '''
        最小二乘法拟合点集为直线
           参数：
              x_ : 拟合好的y值
              y_ : 待拟合y值
           返回:
              k: 直线斜率
              b: 直线偏移
        '''
    k,b = np.polyfit(x_,y_,1)
    k,b = round(k,3),round(b,3)
    return k,b


def pd(centers: list,thr: float) -> int:
    '''
        是否排队  根据多个目标中心点拟合直线，根据r2阈值判断是否排队

        参数：

            centers (list) : [[x1,y1],[x2,y2],[x3,y3],[x4,y4],[x5,y5]]

            thr (float) : 取值范围0~1，越接近1，表示拟合效果越好

        返回：

            return (int) :0 不排队 、1 排队
    '''

    cen = np.array(centers)
    x_ = np.array(cen[:, 0])
    y_ = np.array(cen[:, 1])
    k,b = fit_line(x_, y_)
    y_fit = k*x_+b
    if (goodness_of_fit(y_fit,y_)>thr):
        return 1
    return 0





def update_index_buffer(key: str,
                        value: tuple) -> None:
    """
    向buffer里存放bbox中心点的坐标, buffer 的长度是10帧,目的是防止识别模型检测的抖动现象。

    参数：
        key: key
        value: value

    返回：
        None
    """
    if len(index_buffer[key]) < 10:
        index_buffer[key].append(value)
    else:
        index_buffer[key].pop(0)
        index_buffer[key].append(value)


def segment_detect(gray: np.ndarray) -> tuple:
    """
    利用霍夫曼直线检测原理，检测指针的直线特征

    参数：
        gray (ndarray): 指针的patch

    返回：
        4darray: 线段的起止点坐标
    """
    minValue = 50
    maxValue = 70
    SobelKernel = 3
    minLineLength = 50 # height/32
    maxLineGap = 10 # height/40

    edges = cv2.Canny(gray, minValue, maxValue, apertureSize=SobelKernel)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, minLineLength=minLineLength, maxLineGap=maxLineGap)
    return lines[0]


def line_segment_inter(line: tuple, segment: tuple) -> tuple:
    """
    根据直线的斜截距方程,求直线和线段的交点

    参数：
        line (tuple): x0, y0, x1, y1
        segment (tuple): xs, ys, xe, ye
    
    返回：
        tuple: x, y
    """
    x0, y0, x1, y1 = np.squeeze(line)
    xa, ya, xb, yb = segment
    k_line = (y0 - y1) / (x0 - x1 + 1e-6)
    b_line = y0 - k_line * x0
    delta_ya = k_line * (xa - x0) + y0 - ya
    delta_yb = k_line * (xb - x0) + y0 - yb
    if delta_ya == 0:
        return xa, ya
    if delta_yb == 0:
        return xb, yb
    
    if delta_ya * delta_yb > 0:
        return -1, -1
    else:
        k_segment = (ya - yb) / (xa - xb + 1e-6)
        b_segment = ya - k_segment * xa
        x_inter = (b_segment - b_line) / (k_line - k_segment + 1e-6)
        y_inter = k_line * x_inter + b_line
        return x_inter, y_inter


def show_reading(seg: tuple,
                inter: tuple,
                index: int) -> float:
    """
    根据起止点的坐标,指针与起止点之间连线的交点,以及起止点所对应的刻度值,按照交点所对应的比例,还原出指针对应的读数。

    参数：
        seg (tuple or list): (start_x, start_y, end_x, end_y)
        inter (tuple): (x, y)
        index (int): int

    返回：
        reading (float): float
    """
    xs, ys, xe, ye = seg
    x0, y0 = inter
    ratio = np.linalg.norm((x0 - xs, y0 - ys)) / np.linalg.norm((xe - xs, ye - ys))
    scale_min, scale_max = reading_list[index]
    reading = scale_min + ratio * (scale_max - scale_min)
    return reading


def get_coor(obj: dict,
             img_shape: tuple) -> tuple:
    """
    将相对坐标转换成绝对坐标。

    参数：
        obj (dict): {"class_id": , "name": "", "relative_coordinates": {"center_x": , "center_y": , "width": , "height": }, "confidence": } 
        img_shape (tuple): 视频帧的分辨率， (frame_width, frame_height)

    返回：
        tuple: cx, cy, w, h
    """
    cx = obj['relative_coordinates']['center_x'] * img_shape[0]
    cy = obj['relative_coordinates']['center_y'] * img_shape[1]
    w = obj['relative_coordinates']['width'] * img_shape[0]
    h = obj['relative_coordinates']['height'] * img_shape[1]
    return cx, cy, w, h


def topological_reading(objects: list,
                        patch: np.ndarray,
                        img_shape: tuple) -> float:
    """
    识别仪表盘显示的读数。
    
    参数：
        objects (class list): list 里面存放了多个类,每个类里面保存了关于这个bbox的信息。[{"class_id": , "name": "", "relative_coordinates": {"center_x": , "center_y": , "width": , "height": }, "confidence": }, ...]
        patch (np.ndarray): 使用opencv读取图像后的ndarray格式。
        img_shape (tuple): 视频帧的分辨率， (frame_width, frame_height)
    
    返回：
        reading (float): 最终的读数
    """

    # 用来存放刻度的坐标
    bboxs = [(0, 0, 0, 0)] + [(0, 0) for i in range(6)]
    # 用来表示刻度围成的多边形区域
    reading_heatmap = []
    # 提取信息
    for obj in objects:
        if obj["name"] == "Zhizhen":
            cx, cy, w, h = get_coor(obj, img_shape)
            bboxs[0] = (cx, cy, w, h)

        if obj["name"] == "0":
            cx, cy, w, h = get_coor(obj, img_shape)
            bboxs[1] = (cx, cy)

            update_index_buffer("0", (cx, cy))

            bc_0 = (cx, int(min(cy + h/2, img_shape[1])))
            br_0 = (int(min(cx + w/2, img_shape[0])), int(min(cy + h/2, img_shape[1])))
            reading_heatmap.extend([bc_0, br_0])

        if obj["name"] == "05":
            cx, cy, w, h = get_coor(obj, img_shape)
            bboxs[2] = (cx, cy)

            update_index_buffer("0.5", (cx, cy))
            
            bc_05 = (cx, int(min(cy + h/2, img_shape[1])))
            reading_heatmap.append(bc_05)

        if obj["name"] == "1":
            cx, cy, w, h = get_coor(obj, img_shape)
            bboxs[3] = (cx, cy)

            update_index_buffer("1", (cx, cy))

            lc_1 = (int(max(0, cx - w/2)), cy)
            reading_heatmap.append(lc_1)

        if obj["name"] == "15":
            cx, cy, w, h = get_coor(obj, img_shape)
            bboxs[4] = (cx, cy)

            update_index_buffer("1.5", (cx, cy))

            lc_15 = (int(max(0, cx - w/2)), cy)
            reading_heatmap.append(lc_15)

        if obj["name"] == "2":
            cx, cy, w, h = get_coor(obj, img_shape)
            bboxs[5] = (cx, cy)
            
            update_index_buffer("2", (cx, cy))

            tc_2 = (cx, int(max(0, cy - h/2)))
            reading_heatmap.append(tc_2)

        if obj["name"] == "25":
            cx, cy, w, h = get_coor(obj, img_shape)
            bboxs[6] = (cx, cy)

            update_index_buffer("2.5", (cx, cy))

            tr_25 = (int(min(cx + w/2, img_shape[0])), int(max(0, cy - h/2)))
            br_25 = (int(min(cx + w/2, img_shape[0])), int(min(cy + h/2, img_shape[1])))
            reading_heatmap.extend([tr_25, br_25])

    bboxs = [int(item) for box in bboxs for item in box]

    assert bboxs[:4] != [0, 0, 0, 0], "通用模型无法检测到指针"

    # 获得指针左上角和右下角的坐标
    cx, cy, w, h = bboxs[:4]
    t, l, b, r = max(0, cx - w/2), max(0, cy - h/2), min(img_shape[0], cx + w/2), min(img_shape[1], cy + h/2)
    t, l, b, r = [int(item) for item in [t, l, b, r]]
    # 霍夫曼直线检测
    line = segment_detect(patch)
    tl = np.array([t, l, t, l])
    # 将patch坐标转成图像坐标
    line = line + tl
    # 用来存放数字区域的中心位置
    scales = [(0, 0) for _ in range(6)]
    for index, item in enumerate(scale_list):
        scales[index] = np.mean(np.array(index_buffer[item]), axis=0)
    # 计算指针与读数片段的交点
    nums = len(scales)
    keep_inter = []
    keep_reading = []
    for i in range(nums - 1):
        if np.max(scales[i]) != 0 and np.max(scales[i+1]) != 0:
            seg = (scales[i][0], scales[i][1], scales[i+1][0], scales[i+1][1])
            inter_point = line_segment_inter(line, seg)
            if inter_point != (-1, -1):
                reading = show_reading(seg, inter_point, i)
                keep_inter.append(inter_point)
                keep_reading.append(reading)
        else:
            if np.max(scales[i]) == 0:
                print("识别模型无法识别 {} !!".format(scale_list[i]))
                sys.stdout.flush()
            if np.max(scales[i+1]) == 0:
                print("识别模型无法识别 {} !!".format(scale_list[i+1]))
                sys.stdout.flush()
    # 过滤交点
    # 获得指针bbox四个边的中心点
    bbox_edge_center = [(cx, l),
                        (b, cy),
                        (cx, r),
                        (t, cy)]
    # 判断四个边的中点哪个不在指针读数围成的区域内，那个中点就是指针的方向
    anchor = []
    for tx, ty in bbox_edge_center:
        if not pnpoly(reading_heatmap, tx, ty):
            anchor.append((tx, ty))

    assert len(anchor) == 1, "无法获得指针的方向"

    anchor = np.array(anchor[0])
    keep_inter = np.array(keep_inter)
    dist = np.linalg.norm(anchor - keep_inter, axis=1)
    keep_index = np.argmin(dist)
    ret_reading = keep_reading[keep_index]
    return ret_reading

if __name__ == '__main__':
    # persons_coords = [[0.1, 0.2, 0.2, 0.4]]
    # areas = [[0, 0], [0.1920, 0], [1920, 1080], [0, 1080]]
    # resolution = [1920, 1080]
    # print(
    #     persons_in_areas(persons_coords=persons_coords,
    #                      areas=areas,
    #                      w_thresh=0.3))
    target_area = np.array([[0, 0], [100, 0], [100, 100], [0, 100]])
    coords = np.array([[[50, 50], [100, 100]], [[0, 0], [80, 80]],
                       [[0, 0], [5, 5]]])
    number, density = compute_density(target_area, coords)
    print(number, density, number * density)
    iou = get_IOU(np.array([50, 50, 100, 100]), np.array([0, 0, 100, 100]))
    print(iou)

    basis_x = [i for i in range(5)]
    basis_y = [0 for i in range(5)]
    cur_x = [i for i in range(5)]
    cur_y = [i for i in range(5)]
    res = get_scan_area(basis_x, basis_y, cur_x, cur_y, 2)
    print(res)