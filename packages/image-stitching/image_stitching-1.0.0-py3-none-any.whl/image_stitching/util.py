import cv2
import numpy as np
import os
import re
from image_stitching import exceptions

# MINIMUM_MATCH_POINTS = 20
# CONFIDENCE_THRESH = 65 # 用于同源计算的匹配点的置信度百分比阈值
MINIMUM_MATCH_POINTS = 0 # 最小匹配点
CONFIDENCE_THRESH = 3 # 用于同源计算的匹配点的置信度百分比阈值

def get_matches(img_a_gray, img_b_gray, num_keypoints=1000, threshold=0.8):
    '''使用ORB从两幅图像中获取匹配关键点的函数

    参数：
        img_a_gray (numpy array): 代表灰度图像A的形状（H, W）。
        img_b_gray (numpy array): 代表灰度图像B的形状（H, W）。
        num_keypoints (int)：要匹配的点的数量（默认=100）
        threshold (float): 可以用来只过滤强匹配。值越低，要求越强，因此匹配的数量越少。
    返回：
        match_points_a (numpy array): 形状为(n, 2)，代表图像A关键点的x, y像素坐标。
        match_points_b (numpy array): 形状（n, 2）代表图像B中匹配的关键点的x,y像素坐标。
    '''
    orb = cv2.ORB_create(nfeatures=num_keypoints)
    kp_a, desc_a = orb.detectAndCompute(img_a_gray, None)
    kp_b, desc_b = orb.detectAndCompute(img_b_gray, None)
    
    dis_matcher = cv2.BFMatcher(cv2.NORM_HAMMING)
    matches_list = dis_matcher.knnMatch(desc_a, desc_b, k=2) # 得到图像A中每个关键点的两个最近的匹配点

    # 对于图像A中的每个关键点特征，比较图像B中两个匹配关键点的距离
    # 只有当距离小于阈值时才予以保留
    good_matches_list = []
    for match_1, match_2 in matches_list:
        if match_1.distance < threshold * match_2.distance:
            good_matches_list.append(match_1)
    
    #筛选出好的匹配关键点
    good_kp_a = []
    good_kp_b = []

    for match in good_matches_list:
        good_kp_a.append(kp_a[match.queryIdx].pt) # keypoint in image A
        good_kp_b.append(kp_b[match.trainIdx].pt) # 图像B中匹配的关键点
    
    if len(good_kp_a) < MINIMUM_MATCH_POINTS:
        raise exceptions.NotEnoughMatchPointsError(len(good_kp_a), MINIMUM_MATCH_POINTS)
    
    return np.array(good_kp_a), np.array(good_kp_b)


def calculate_homography(points_img_a, points_img_b):
    '''使用直接线性变换从点的对应关系中计算同源矩阵的功能
        结果同源矩阵将图像B中的点转化为图像A中的点
        同源矩阵H = [h1 h2 h3；
                        h4 h5 h6；
                        h7 h8 h9] 。
        u, v ---> 图像A中的点
        x, y ---> 图像B中的匹配点，然后、
        n个点的对应，DLT方程为：
            A.h = 0
        其中A = [-x1 -y1 -1 0 0 0 u1*x1 u1*y1 u1；
                   0 0 0 -x1 -y1 -1 v1*x1 v1*y1 v1；
                   ...............................;
                   ...............................;
                   -xn -yn -1 0 0 0 un*xn un*yn un；
                   0 0 0 -xn -yn -1 vn*xn vn*yn vn] 。
        然后用SVD解决这个方程
        (至少需要4个点的对应关系来确定同源矩阵的8个非kwown参数)
    Args：
        points_img_a (numpy array): 形状(n, 2)代表图像A中的像素坐标点(u, v)。
        points_img_b (numpy array): 形状(n, 2)，代表图像B中的像素坐标点(x, y)

    返回：
        h_mat： 一个(3, 3)的小数组，用于估计同构图。
    '''
    # concatenate the two numpy points array to get 4 columns (u, v, x, y)
    points_a_and_b = np.concatenate((points_img_a, points_img_b), axis=1)
    A = []
    # fill the A matrix by looping through each row of points_a_and_b containing u, v, x, y
    # each row in the points_ab would fill two rows in the A matrix
    for u, v, x, y in points_a_and_b:
        A.append([-x, -y, -1, 0, 0, 0, u*x, u*y, u])
        A.append([0, 0, 0, -x, -y, -1, v*x, v*y, v])
    
    A = np.array(A)
    _, _, v_t = np.linalg.svd(A)

    # soltion is the last column of v which means the last row of its transpose v_t
    h_mat = v_t[-1, :].reshape(3,3)
    return h_mat

def transform_with_homography(h_mat, points_array):
    """使用给定的同源矩阵转换一组点的函数。
        变换后的点被归一化，最后一列代表比例。

    参数：
        h_mat (numpy array): 形状为(3, 3)，代表同源矩阵。
        points_array (numpy array): 形状为(n, 2)，代表n组x, y像素的坐标。
            要被转换的x、y像素坐标
    """
    # add column of ones so that matrix multiplication with homography matrix is possible
    ones_col = np.ones((points_array.shape[0], 1))
    points_array = np.concatenate((points_array, ones_col), axis=1)
    transformed_points = np.matmul(h_mat, points_array.T)
    epsilon = 1e-7 # very small value to use it during normalization to avoid division by zero
    transformed_points = transformed_points / (transformed_points[2,:].reshape(1,-1) + epsilon)
    transformed_points = transformed_points[0:2,:].T
    return transformed_points


def compute_outliers(h_mat, points_img_a, points_img_b, threshold=6):
    '''用图像A和图像B中的匹配点计算同源矩阵误差的函数。
        图像A和图像B中的匹配点，计算同源矩阵的误差。

    参数：
        h_mat (numpy array): 形状(3, 3)，代表将图像B中的点转换为图像A中的点的同源矩阵。
        points_img_a (numpy array): 形状(n, 2)代表图像A中的像素坐标点(u, v)。
        points_img_b (numpy array): 形状(n, 2)，代表图像B中的像素坐标点(x, y)
        theshold (int): 3一个数字，代表图像B中转换后的像素坐标与匹配的像素坐标之间允许的欧几里得距离（以像素计）。
            与图像A中相匹配的像素坐标之间的允许的欧几里得距离，将其作为离群值。

    返回：
        error：一个标量的浮点数，代表Homography矩阵中的误差。
    '''
    num_points = points_img_a.shape[0]
    outliers_count = 0

    # transform the match point in image B to image A using the homography
    points_img_b_hat = transform_with_homography(h_mat, points_img_b)
    
    # let x, y be coordinate representation of points in image A
    # let x_hat, y_hat be the coordinate representation of transformed points of image B with respect to image A
    x = points_img_a[:, 0]
    y = points_img_a[:, 1]
    x_hat = points_img_b_hat[:, 0]
    y_hat = points_img_b_hat[:, 1]
    euclid_dis = np.sqrt(np.power((x_hat - x), 2) + np.power((y_hat - y), 2)).reshape(-1)
    for dis in euclid_dis:
        if dis > threshold:
            outliers_count += 1
    return outliers_count


def compute_homography_ransac(matches_a, matches_b):
    """用RANSAC估计潜在匹配点的最佳同源矩阵的函数。
    点。

    Args：
        matches_a (numpy数组): 形状为(n, 2)，代表图像A中可能匹配点的坐标。
            代表图像A中可能的匹配点的坐标
        matches_b (numpy array): 形状(n, 2)，代表图像B中可能匹配点的坐标。
            代表图像B中可能的匹配点的坐标

    返回：
        best_h_mat： 形状为(3, 3)的numpy数组，代表最佳同源矩阵。
            矩阵，将图像B中的点转换为图像A中的点。
    """
    num_all_matches =  matches_a.shape[0]
    # RANSAC parameters
    SAMPLE_SIZE = 5 # number of point correspondances for estimation of Homgraphy
    SUCCESS_PROB = 0.995 # required probabilty of finding H with all samples being inliners
    min_iterations = int(np.log(1.0 - SUCCESS_PROB)/np.log(1 - 0.5**SAMPLE_SIZE))
    
    # Let the initial error be large i.e consider all matched points as outliers
    lowest_outliers_count = num_all_matches
    best_h_mat = None
    best_i = 0 # just to know in which iteration the best h_mat was found

    for i in range(min_iterations):
        rand_ind = np.random.permutation(range(num_all_matches))[:SAMPLE_SIZE]
        h_mat = calculate_homography(matches_a[rand_ind], matches_b[rand_ind])
        outliers_count = compute_outliers(h_mat, matches_a, matches_b)
        if outliers_count < lowest_outliers_count:
            best_h_mat = h_mat
            lowest_outliers_count = outliers_count
            best_i = i
    best_confidence_obtained = int(100 - (100 * lowest_outliers_count / num_all_matches))
    if best_confidence_obtained < CONFIDENCE_THRESH:
        raise(exceptions.MatchesNotConfident(best_confidence_obtained))
    return best_h_mat


def get_corners_as_array(img_height, img_width):
    """函数从图像的宽度和高度中提取角点，并将其排列成
        数组的形式。

        4个角的排列方式如下：
        corners = [top_left_x, top_left_y；
                   top_right_x, top_right_y；
                   bottom_right_x, bottom_right_y；
                   bottom_left_x, bottom_left_y］。

    Args：
        img_height (str): 图片的高度
        img_width (str): 图片的宽度

    返回：
        corner_points_array (numpy array): 形状为(4,2)的数组，代表角的x,y像素坐标。
    """
    corners_array = np.array([[0, 0],
                            [img_width - 1, 0],
                            [img_width - 1, img_height - 1],
                            [0, img_height - 1]])
    return corners_array


def get_crop_points_horz(img_a_h, transfmd_corners_img_b):
    """功能，在水平缝合的图像中找到像素角，以裁剪和删除
        周围的黑色空间。

    参数：
        img_a_h (int): 枢轴图像的高度，即图像A。
        transfmd_corners_img_b (numpy array): 形状为(n, 2)，代表图像B的转换角。
            这些角需要按以下顺序排列：
            corners = [top_left_x, top_left_y；
                   top_right_x, top_right_y；
                   bottom_right_x, bottom_right_y；
                   bottom_left_x, bottom_left_y］。
    返回：
        x_start (int): 缝合后的图像上开始裁剪的x像素坐标。
        y_start (int): 缝合后的图像上开始裁剪的x像素坐标。
        x_end (int): 缝合后的图像上结束裁剪的x像素坐标
        y_end (int): 缝合后的图像结束的y像素坐标。
    """
    # the four transformed corners of image B
    top_lft_x_hat, top_lft_y_hat = transfmd_corners_img_b[0, :]
    top_rht_x_hat, top_rht_y_hat = transfmd_corners_img_b[1, :]
    btm_rht_x_hat, btm_rht_y_hat = transfmd_corners_img_b[2, :]
    btm_lft_x_hat, btm_lft_y_hat = transfmd_corners_img_b[3, :]

    # initialize the crop points
    # since image A (on the left side) is used as pivot, x_start will always be zero
    x_start, y_start, x_end, y_end = (0, None, None, None)

    if (top_lft_y_hat > 0) and (top_lft_y_hat > top_rht_y_hat):
        y_start = top_lft_y_hat
    elif (top_rht_y_hat > 0) and (top_rht_y_hat > top_lft_y_hat):
        y_start = top_rht_y_hat
    else:
        y_start = 0
        
    if (btm_lft_y_hat < img_a_h - 1) and (btm_lft_y_hat < btm_rht_y_hat):
        y_end = btm_lft_y_hat
    elif (btm_rht_y_hat < img_a_h - 1) and (btm_rht_y_hat < btm_lft_y_hat):
        y_end = btm_rht_y_hat
    else:
        y_end = img_a_h - 1

    if (top_rht_x_hat < btm_rht_x_hat):
        x_end = top_rht_x_hat
    else:
        x_end = btm_rht_x_hat
    
    return int(x_start), int(y_start), int(x_end), int(y_end)


def get_crop_points_vert(img_a_w, transfmd_corners_img_b):
    """找到垂直缝合的图像中的像素角的功能，以裁剪和删除
        周围的黑色空间。

    参数：
        img_a_h (int): 枢轴图像的宽度，即图像A。
        transfmd_corners_img_b (numpy array): 形状为(n, 2)，代表图像B的转换角。
            这些角需要按以下顺序排列：
            corners = [top_left_x, top_left_y；
                   top_right_x, top_right_y；
                   bottom_right_x, bottom_right_y；
                   bottom_left_x, bottom_left_y］。
    返回：
        x_start (int): 缝合后的图像上开始裁剪的x像素坐标。
        y_start (int): 缝合后的图像上开始裁剪的x像素坐标。
        x_end (int): 缝合后的图像上结束裁剪的x像素坐标
        y_end (int): 缝合后的图像结束的y像素坐标。
    """
    # the four transformed corners of image B
    top_lft_x_hat, top_lft_y_hat = transfmd_corners_img_b[0, :]
    top_rht_x_hat, top_rht_y_hat = transfmd_corners_img_b[1, :]
    btm_rht_x_hat, btm_rht_y_hat = transfmd_corners_img_b[2, :]
    btm_lft_x_hat, btm_lft_y_hat = transfmd_corners_img_b[3, :]

    # initialize the crop points
    # since image A (on the top) is used as pivot, y_start will always be zero
    x_start, y_start, x_end, y_end = (None, 0, None, None)

    if (top_lft_x_hat > 0) and (top_lft_x_hat > btm_lft_x_hat):
        x_start = top_lft_x_hat
    elif (btm_lft_x_hat > 0) and (btm_lft_x_hat > top_lft_x_hat):
        x_start = btm_lft_x_hat
    else:
        x_start = 0
        
    if (top_rht_x_hat < img_a_w - 1) and (top_rht_x_hat < btm_rht_x_hat):
        x_end = top_rht_x_hat
    elif (btm_rht_x_hat < img_a_w - 1) and (btm_rht_x_hat < top_rht_x_hat):
        x_end = btm_rht_x_hat
    else:
        x_end = img_a_w - 1

    if (btm_lft_y_hat < btm_rht_y_hat):
        y_end = btm_lft_y_hat
    else:
        y_end = btm_rht_y_hat
    
    return int(x_start), int(y_start), int(x_end), int(y_end)


def get_crop_points(h_mat, img_a, img_b, stitch_direc):
    """查找像素角的函数，以裁剪缝合后的图像，使缝合后的图像中的黑色空间被去除。
        缝合后的图像中的黑色空间被移除。
        黑空间可能是因为图像B与图像A的尺寸不一致
        或者图像B在同位素转换后出现了倾斜。
        例子：
                  (水平缝合)
                ____________                     _________________
                |           |                    |                |
                |           |__________          |                |
                |           |         /          |       A        |
                |     A     |   B    /           |________________|
                |           |       /                |          | 
                |           |______/                 |    B     |
                |___________|                        |          |
                                                     |__________|  <-想象一下倾斜的底边
        
        这个函数返回角点，以获得A和B内部的最大面积，并确保
        确保边缘是直的（即水平和垂直的）。

    参数：
        h_mat (numpy array): 形状为(3, 3)，代表从图像B到图像A的同构图。
        img_a (numpy array): 形状(h, w, c)代表图像A
        img_b (numpy array): 代表图像B的形状(h, w, c)。
        stitch_direc（int）： 纵向缝合时为0，横向缝合时为1。

    返回：
        x_start (int): 缝合后的图像上开始裁剪的x像素坐标。
        y_start (int): 缝合后的图像上开始裁剪的x像素坐标。
        x_end (int): 缝合后的图像上结束裁剪的x像素坐标
        y_end (int): 缝合后的图像结束的y像素坐标。
    """
    img_a_h, img_a_w, _ = img_a.shape
    img_b_h, img_b_w, _ = img_b.shape

    orig_corners_img_b = get_corners_as_array(img_b_h, img_b_w)
                
    transfmd_corners_img_b = transform_with_homography(h_mat, orig_corners_img_b)

    if stitch_direc == 1:
        x_start, y_start, x_end, y_end = get_crop_points_horz(img_a_w, transfmd_corners_img_b)
    # initialize the crop points
    x_start = None
    x_end = None
    y_start = None
    y_end = None

    if stitch_direc == 1: # 1 is horizontal
        x_start, y_start, x_end, y_end = get_crop_points_horz(img_a_h, transfmd_corners_img_b)
    else: # when stitching images in the vertical direction
        x_start, y_start, x_end, y_end = get_crop_points_vert(img_a_w, transfmd_corners_img_b)
    return x_start, y_start, x_end, y_end


def stitch_image_pair(img_a, img_b, stitch_direc):
    """功能是将图像B沿所述方向缝合到图像A上。

    参数：
        img_a (numpy array): 形状(H, W, C)与图像A的opencv表示(即C: B,G,R)
        img_b (numpy array): 形状(H, W, C)和图像B的opencv表示(即C: B,G,R)
        stitch_direc (int)： 0表示垂直缝合，1表示水平缝合

    返回：
        stitched_image (numpy array): 裁剪后的图像A和图像B的最大内容的缝合图。
            以去除黑色空间
    """
    img_a_gray = cv2.cvtColor(img_a, cv2.COLOR_BGR2GRAY)
    img_b_gray = cv2.cvtColor(img_b, cv2.COLOR_BGR2GRAY)
    matches_a, matches_b = get_matches(img_a_gray, img_b_gray, num_keypoints=1000, threshold=0.8)
    h_mat = compute_homography_ransac(matches_a, matches_b)
    if stitch_direc == 0:
        canvas = cv2.warpPerspective(img_b, h_mat, (img_a.shape[1], img_a.shape[0] + img_b.shape[0]))
        canvas[0:img_a.shape[0], :, :] = img_a[:, :, :]
        x_start, y_start, x_end, y_end = get_crop_points(h_mat, img_a, img_b, 0)
    else:
        canvas = cv2.warpPerspective(img_b, h_mat, (img_a.shape[1] + img_b.shape[1], img_a.shape[0]))
        canvas[:, 0:img_a.shape[1], :] = img_a[:, :, :]
        x_start, y_start, x_end, y_end = get_crop_points(h_mat, img_a, img_b, 1)
    
    stitched_img = canvas[y_start:y_end,x_start:x_end,:]
    return stitched_img


def check_imgfile_validity(folder, filenames):
    """检查给定路径中的文件是否为有效图像文件的函数。

    参数：
        folder (str): 包含图像文件的路径
        filenames (list): 图像文件名的列表

    返回：
        valid_files (bool)： 如果所有的文件都是有效的图像文件则为真，否则为假
        msg (str)： 必须显示的错误信息
    """
    for file in filenames:
        full_file_path = os.path.join(folder, file)
        regex = "([^\\s]+(\\.(?i:(jpe?g|png)))$)"
        p = re.compile(regex)

        if not os.path.isfile(full_file_path):
            return False, "File not found: " + full_file_path
        if not (re.search(p, file)):
            return False, "Invalid image file: " + file
    return True, None
