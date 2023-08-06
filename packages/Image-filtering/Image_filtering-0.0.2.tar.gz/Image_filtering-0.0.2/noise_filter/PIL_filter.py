from PIL import Image, ImageFilter
from scipy.ndimage import filters
import numpy as np

# 中值滤波
def Pre_median_filters(img_path, size=3):
    from PIL import Image, ImageFilter
    # img = Image.open(img_path)
    res = img_path.filter(ImageFilter.MedianFilter(size=size))
    return res


def median_filter(image):
    import cv2 as cv
    # 将图像数据数组转换为PIL的Image对象
    pil_image = Image.fromarray(cv.cvtColor(image, cv.COLOR_BGR2RGB))

    filtered_image = Pre_median_filters(pil_image)
    # 将中值滤波后的图像转换为numpy数组
    filtered_image_array = cv.cvtColor(np.array(filtered_image), cv.COLOR_RGB2BGR)
    return filtered_image_array


# 高斯滤波
def Pre_gaussian_filters(image, radius=2):
    from PIL import Image, ImageFilter
    # img = Image.open(img_path)
    res = image.filter(ImageFilter.GaussianBlur(radius=radius))
    return res

def gaussian_filter(image):
    import cv2 as cv
    # 将图像数据数组转换为PIL的Image对象
    pil_image = Image.fromarray(cv.cvtColor(image, cv.COLOR_BGR2RGB))

    filtered_image = Pre_gaussian_filters(pil_image)
    # 将中值滤波后的图像转换为numpy数组
    filtered_image_array = cv.cvtColor(np.array(filtered_image), cv.COLOR_RGB2BGR)
    return filtered_image_array


# 拉普拉斯滤波
def Pre_laplace_filters(image):
    from PIL import Image, ImageFilter
    # img = Image.open(img_path)
    res = image.filter(ImageFilter.Kernel((3, 3), (-1, -1, -1, -1, 8, -1, -1, -1, -1), 1, 0))
    return res


def laplace_filter(image):
    import cv2 as cv
    # 将图像数据数组转换为PIL的Image对象
    pil_image = Image.fromarray(cv.cvtColor(image, cv.COLOR_BGR2RGB))

    filtered_image = Pre_laplace_filters(pil_image)
    # 将中值滤波后的图像转换为numpy数组
    filtered_image_array = cv.cvtColor(np.array(filtered_image), cv.COLOR_RGB2BGR)
    return filtered_image_array


# 模糊滤波
def Pre_blur_filters(image):
    from PIL import Image, ImageFilter
    # img = Image.open(img_path)
    res = image.filter(ImageFilter.BLUR)
    return res

def blur_filter(image):
    import cv2 as cv
    # 将图像数据数组转换为PIL的Image对象
    pil_image = Image.fromarray(cv.cvtColor(image, cv.COLOR_BGR2RGB))

    filtered_image = Pre_blur_filters(pil_image)
    # 将中值滤波后的图像转换为numpy数组
    filtered_image_array = cv.cvtColor(np.array(filtered_image), cv.COLOR_RGB2BGR)
    return filtered_image_array


def bilateral_funcs(pixels, sigma_color):
    """
    自定义的双边滤波函数
    """

    center_pixel = pixels[int(len(pixels) / 2)]
    weight = np.exp(-((pixels - center_pixel) ** 2) / (2 * sigma_color ** 2))
    weighted_pixels = weight * pixels
    return np.sum(weighted_pixels) / np.sum(weight)

# 双边滤波
def Pre_bilateral_filter(image, size=11, sigma_space=3, sigma_color=0.1):
    # 打开图像文件并转化为灰度图
    # img = Image.open(image_path).convert('L')
    from PIL import Image, ImageFilter
    # 转换为灰度图像
    img = image.convert('L')

    # 将图像转换为numpy数组
    img_array = np.array(img)

    # 对图像进行双边滤波处理
    result = filters.gaussian_filter(img_array, sigma=sigma_space)
    result = filters.generic_filter(result, function=bilateral_funcs, size=size, extra_arguments=(sigma_color,))

    # 将处理后的numpy数组转化为图像
    result_img = Image.fromarray(np.uint8(result))

    return result_img

def bilateral_filter(image):
    import cv2 as cv
    # 将图像数据数组转换为PIL的Image对象
    pil_image = Image.fromarray(cv.cvtColor(image, cv.COLOR_BGR2RGB))

    filtered_image = Pre_bilateral_filter(pil_image)
    # 将中值滤波后的图像转换为numpy数组
    filtered_image_array = cv.cvtColor(np.array(filtered_image), cv.COLOR_RGB2BGR)
    return filtered_image_array



# 小波变换去噪
def Pre_WLS_filters(image):
    from PIL import Image, ImageFilter
    # img = Image.open(img_path)

    unsharp_mask_filter = ImageFilter.UnsharpMask(radius=10, percent=200, threshold=3)
    unsharp_mask = image.filter(unsharp_mask_filter)

    return unsharp_mask

def WLS_filter(image):
    import cv2 as cv
    # 将图像数据数组转换为PIL的Image对象
    pil_image = Image.fromarray(cv.cvtColor(image, cv.COLOR_BGR2RGB))

    filtered_image = Pre_WLS_filters(pil_image)
    # 将中值滤波后的图像转换为numpy数组
    filtered_image_array = cv.cvtColor(np.array(filtered_image), cv.COLOR_RGB2BGR)
    return filtered_image_array


# nl_means滤波
def Pre_nl_means_filters(image, patch_size=5, window_size=11, h=5):
    from PIL import Image, ImageFilter
    # 读取图像
    # img = Image.open(image_path)
    # 转换为灰度图像
    img = image.convert('L')
    # 转换为numpy数组
    img_array = np.array(img, dtype=np.float64)

    # 获取图像尺寸
    height, width = img_array.shape
    # 计算窗口半径
    window_radius = window_size // 2
    # 计算块半径
    patch_radius = patch_size // 2

    # 复制原始图像
    result_img = np.copy(img_array)

    # 计算所有块的均值
    mean_patch = np.zeros((height, width, patch_size, patch_size))
    for i in range(patch_radius, height - patch_radius):
        for j in range(patch_radius, width - patch_radius):
            mean_patch[i, j, :, :] = img_array[i - patch_radius:i + patch_radius + 1,
                                     j - patch_radius:j + patch_radius + 1]

    # 计算每个像素的加权平均值
    for i in range(window_radius, height - window_radius):
        for j in range(window_radius, width - window_radius):
            # 计算搜索窗口
            window = img_array[i - window_radius:i + window_radius + 1,
                     j - window_radius:j + window_radius + 1]
            # 计算所有搜索窗口中块的相似度
            weights = np.exp(-np.sum((mean_patch[i, j, :, :] - mean_patch[i - patch_radius:i + patch_radius + 1,
                                                               j - patch_radius:j + patch_radius + 1]) ** 2
                                     / (h ** 2)) / window_size ** 2)
            # 计算总权值
            total_weights = np.sum(weights)
            # 计算加权平均值并将其赋值给结果图像
            result_img[i, j] = np.sum(weights * window) / total_weights

    # 将结果图像转换为PIL图像
    result_img = Image.fromarray(np.uint8(result_img))
    return result_img


def nl_means_filter(image):
    import cv2 as cv
    # 将图像数据数组转换为PIL的Image对象
    pil_image = Image.fromarray(cv.cvtColor(image, cv.COLOR_BGR2RGB))

    filtered_image = Pre_nl_means_filters(pil_image)
    # 将中值滤波后的图像转换为numpy数组
    filtered_image_array = cv.cvtColor(np.array(filtered_image), cv.COLOR_RGB2BGR)
    return filtered_image_array