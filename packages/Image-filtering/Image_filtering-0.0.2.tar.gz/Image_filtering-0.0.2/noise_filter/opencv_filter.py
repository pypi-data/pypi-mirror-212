import numpy as np
from matplotlib import pyplot as plt

# 均值滤波器
def average_filter(imageNoise):	    # imageNoise ： 噪声图片
    import cv2 as cv
    # 均值滤波
    img_blur = cv.blur(imageNoise, (5, 5))
    return img_blur


# 高斯滤波器
def gaussian_filter(src, k_size=(3, 3), sigma=1.5):
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

#双边滤波器
def bilateral_filter(img):
    # 进行双边滤波
    # 双边滤波能在保持边界清晰的情况下有效的去除噪音。但是这种操作与其他滤波器相比会比较慢.
    import cv2 as cv
    blurred = cv.bilateralFilter(img, 7, 50, 50)
    return blurred

#形态学去噪滤波器
def Morphological_filter(img):
    import cv2 as cv
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    opening = cv.morphologyEx(img, cv.MORPH_OPEN, kernel)
    closing = cv.morphologyEx(opening, cv.MORPH_CLOSE, kernel)
    return closing

# 非局部均值（ NLM ）去噪滤波器
def NLM_filter(img):
    # 对图像进行去噪处理
    import cv2 as cv
    dst = cv.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
    return dst

#阈值邻域平滑滤波
def threshAverFilter(img, T=10):
    # 将图像转换为灰度图像
    import cv2 as cv
    imgNoise = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    imgAver = cv.blur(imgNoise, (3, 3))  # 均值滤波
    row, col = imgNoise.shape[:2]
    imgThresh = np.zeros((row, col), dtype=np.uint8)
    for i in range(row):
        for j in range(col):
            # if np.abs(imgNoise[i, j] - imgAver[i, j], dtype=np.int16).any() >= T:
            if np.abs(np.int16(imgNoise[i, j]) - np.int16(imgAver[i, j])).any() >= T:
                imgThresh[i, j] = imgAver[i, j]
            else:
                imgThresh[i, j] = imgNoise[i, j]
    return imgThresh

#方框滤波器
def Box_filter(img):
    # 进行方框滤波
    import cv2 as cv
    kernel_size = 3     # 定义滤波器大小
    img_filtered = cv.boxFilter(img, -1, (kernel_size, kernel_size))
    return img_filtered

#laplacian滤波器
def laplacian_filter(img):
    # 将图像转换为灰度图像
    import cv2 as cv
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # 应用拉普拉斯滤波器进行图像去噪
    laplacian = cv.Laplacian(gray, cv.CV_64F)

    # 将图像转换回灰度图像
    laplacian = np.uint8(np.absolute(laplacian))
    return laplacian

# 边缘保留滤波器
def edge_preserving_filter(img):
    # 边缘保留滤波
    import cv2 as cv
    edge_preserving = cv.edgePreservingFilter(img)
    return edge_preserving


def Pre_fft_filter(img):
    # 将图像转换为灰度图像
    import cv2 as cv
    image = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # 傅里叶变换
    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)

    # 设置高通滤波器
    n = 10
    rows, cols = image.shape
    crow, ccol = rows//2, cols//2
    mask = np.zeros((rows, cols), np.uint8)
    mask[crow-n:crow+n, ccol-n:ccol+n] = 1

    # 将高通滤波器应用于傅里叶变换
    fshift = fshift*mask

    # 傅里叶反变换
    ishift = np.fft.ifftshift(fshift)
    iimg = np.fft.ifft2(ishift)
    iimg = np.abs(iimg)
    return iimg

def fft_filter(image):
    import cv2 as cv
    # 显示和保存傅里叶变换滤波后的图像
    img = Pre_fft_filter(image)
    # 应用颜色映射
    colormap = cv.applyColorMap(img.astype(np.uint8), cv.COLORMAP_JET)
    return colormap
