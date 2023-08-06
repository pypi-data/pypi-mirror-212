class InsufficientImagesError(Exception):
    """
        异常类，当图像数量不足时可被调用。

    参数：
        num_images (int): 图片的数量（这只是用来在信息中显示）。
    """
    def __init__(self, num_images):
        msg = "Expected 2 or more images but got only " +  str(num_images)
        super(InsufficientImagesError, self).__init__(msg)


class InvalidImageFilesError(Exception):
    """异常类，当文件是无效的图像文件或它们不存在时可以被调用。

    Args：
        msg (str)： 错误描述
    """
    def __init__(self, msg):
        super(InvalidImageFilesError, self).__init__(msg)


class NotEnoughMatchPointsError(Exception):
    """异常类，当图像之间没有足够的匹配点时，可以被调用。
        所定义的足够多的匹配点时，可以调用该类。

    参数：
        num_match_points (int): 找到的匹配点的数量
        min_match_points_req (int): 图像之间需要的最小匹配点数量
    """
    def __init__(self, num_match_points, min_match_points_req):
        msg = "There are not enough match points between images in the input images. Required atleast " + \
               str(min_match_points_req) + " matches but could find only " + str(num_match_points) + " matches!"
        super(NotEnoughMatchPointsError, self).__init__(msg)


class MatchesNotConfident(Exception):
    """异常类，当离群匹配数与所有匹配数之比超过最低阈值时，可以调用该类。
        超过最小阈值时，可以调用该类，以自信地计算同源矩阵。

    Args：
        confidence (int): 表示匹配点的置信度的百分比
    """
    def __init__(self, confidence):
        msg = "The confidence in the matches is less than the defined threshold and hence the stitching operation \
        cannot be performed. Perhaps the input images have very less overlapping content to detect good match points!"
        super(MatchesNotConfident, self).__init__(msg + " Confidence: " + str(confidence))