import numpy as np
from matplotlib import pyplot as plt

# 均值滤波器
def average_filter(imageNoise):	    # imageNoise ： 噪声图片
    import cv2 as cv
    # 均值滤波
    img_blur = cv.blur(imageNoise, (5, 5))
    return img_blur


# 高斯滤波器
def gaussian_filter(src, k_size, sigma):
    import cv2 as cv
    img = src.copy()
    # 高斯滤波
    # k_size表示高斯滤波器的长和宽，sigma表示滤波器的标准差
    img_gaussianBlur = cv.GaussianBlur(img, k_size, sigma)
    return img_gaussianBlur

#中值滤波
def median_filter(img):
    import cv2 as cv
    # 对图像进行中值滤波
    median = cv.medianBlur(img, 5)
    return median

