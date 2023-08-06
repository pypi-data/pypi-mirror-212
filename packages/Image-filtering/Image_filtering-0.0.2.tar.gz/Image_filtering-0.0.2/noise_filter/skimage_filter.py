import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import convolve2d
from skimage import io, filters
from PIL import Image, ImageFilter
#方框滤波
def Pre_fangkuang_filter(image):
    import numpy as np
    from scipy.signal import convolve2d

    # 将图像转换为灰度图像
    gray_img = np.mean(image, axis=2)
    # 定义方框滤波器的大小
    k = 5
    # 创建方框滤波器（即均值滤波器）
    kernel = np.ones((k, k)) / k ** 2
    # 应用滤波器
    smoothed_img = convolve2d(gray_img, kernel, mode='same')
    return smoothed_img


def fangkuang_filter(image):
    import cv2 as cv
    # 将图像数据数组转换为PIL的Image对象
    pil_image = Image.fromarray(cv.cvtColor(image, cv.COLOR_BGR2RGB))

    filtered_image = Pre_fangkuang_filter(pil_image)
    # 将中值滤波后的图像转换为numpy数组

    # 将图像的数据类型转换为8-bit unsigned integer
    filtered_image_array = np.array(filtered_image, dtype=np.uint8)
    # 将图像从RGB颜色空间转换为BGR颜色空间
    filtered_image_array = cv.cvtColor(filtered_image_array, cv.COLOR_RGB2BGR)

    # 将中值滤波后的图像转换为numpy数组，并将数据类型转换为8-bit unsigned integer
    # filtered_image_array = cv.cvtColor(np.array(filtered_image), cv.COLOR_RGB2BGR).astype(np.uint8)

    # filtered_image_array = cv.cvtColor(np.array(filtered_image), cv.COLOR_RGB2BGR)

    return filtered_image_array


#高斯滤波
def gaussian_filter(image):
    from skimage import io, filters
    # 高斯滤波器
    gaussian = filters.gaussian(image, sigma=1, channel_axis=-1)

    # gaussian = filters.gaussian(image, sigma=1)
    return gaussian

#均值滤波
def average_filter(image):
    import numpy as np
    # 定义均值核
    kernel = np.ones((3, 3)) / 9
    # 进行均值滤波
    dst = np.zeros_like(image)
    for i in range(3):
        dst[:, :, i] = np.convolve(image[:, :, i].ravel(), kernel.ravel(), mode='same').reshape(
            (image.shape[0], image.shape[1]))
    return dst

def laplace_filter(image):

    from skimage import io, filters
    # 应用 Laplace 滤波器
    laplace_image = filters.laplace(image)
    return laplace_image

def prewitt_filter(image):

    from skimage import io, filters
    # 应用 Prewitt 滤波器
    prewitt_image = filters.prewitt(image)
    return prewitt_image

def scharr_filter(image):

    from skimage import io, filters
    # 应用 Prewitt 滤波器
    prewitt_image = filters.prewitt(image)
    return prewitt_image

def sobel_filter(image):

    from skimage import io, filters
     # 应用 Sobel 滤波器
    sobel_image = filters.sobel(image)
    return sobel_image
