# from . import util
# from . import exceptions
# from .vgg import B2_VGG
# from image_stitching import util
# from image_stitching import exceptions
# import util
# import exceptions
import os
import cv2
import time

from image_stitching import util
from image_stitching import exceptions


def stitch_images(image_folder, image_filenames, stitch_direction):
    """
        缝合一连串输入图像的功能。
        图像可以被水平或垂直地缝合。
        对于水平缝合，图像必须在场景中从左到右的顺序传递。
        对于垂直拼接，图像必须在场景中从上到下的顺序传递。

    参数：
        image_folder (str): 包含图像的目录的路径
        image_filenames (list): 按缝合顺序排列的图像文件名的列表。
        stitch_direction（int）： 1用于水平缝合，0用于垂直缝合

    返回：
        stitched_image (numpy array): 形状为(H, W, 3)，代表缝合后的图像。
    """
    num_images = len(image_filenames)
    
    if num_images < 2:
        raise(exceptions.InsufficientImagesError(num_images))
    
    valid_files, file_error_msg = util.check_imgfile_validity(image_folder, image_filenames)
    if not valid_files:
        raise(exceptions.InvalidImageFilesError(file_error_msg))
    
    pivot_img_path = os.path.join(image_folder, image_filenames[0])
    pivot_img = cv2.imread(pivot_img_path)

    for i in range(1, num_images, 1):
        join_img_path = os.path.join(image_folder, image_filenames[i])
        join_img = cv2.imread(join_img_path)
        pivot_img = util.stitch_image_pair(pivot_img, join_img, stitch_direc=stitch_direction)
    
    return pivot_img

def stitch_images_and_save(image_folder, image_filenames, stitch_direction, output_folder=None):
    """缝合和保存结果图像的功能。
        图像可以被水平或垂直地缝合。
        对于水平缝合，图像必须在场景中从左到右的顺序传递。
        对于垂直拼接，图像必须在场景中从上到下的顺序传递。

    参数：
        image_folder (str): 包含图像的目录的路径
        image_filenames (list): 按缝合顺序排列的图像文件名的列表。
        stitch_direction（int）： 1表示水平缝合，0表示垂直缝合
        output_folder (str): 保存缝合后图像的目录（默认为None，会创建一个名为 "output "的目录来保存）

    返回：
        无
    """
    timestr = time.strftime("%Y%m%d_%H%M%S")
    filename = "stitched_image_" + timestr + ".jpg"
    stitched_img = stitch_images(image_folder, image_filenames, stitch_direction)
    if output_folder is None:
        if not os.path.isdir("output"):
            os.makedirs("output/")
        output_folder = "output"
    full_save_path = os.path.join(output_folder, filename)
    _ = cv2.imwrite(full_save_path, stitched_img)
    print("The stitched image is saved at: " + full_save_path)

