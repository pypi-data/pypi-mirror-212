# package
# __init__.py
import re
import urllib
import sys
import os
# from .noise_filter import average_filter, gaussian_filter, median_filter, bilateral_filter, Morphological_filter, NLM_filter, threshAverFilter, Box_filter, laplacian_filter, edge_preserving_filter, fft_filter, median_filters
# from .PIL_filter import median_filters, gaussian_filters, laplace_filters, blur_filters, bilateral_filters, bilateral_funcs, WLS_filters, nl_means_filters
#
# __all__=["noise_filter"] # 列表可以根据要导入的模块数而进行新增，列表元素是之前新建的py文件的名字
# __all__=["PIL_filter"]
#
from .opencv_filter import average_filter, gaussian_filter, median_filter, bilateral_filter, Morphological_filter, NLM_filter, threshAverFilter, Box_filter, laplacian_filter, edge_preserving_filter, fft_filter
from .PIL_filter import median_filter, gaussian_filter, laplace_filter, blur_filter, bilateral_filter, bilateral_funcs, WLS_filter, nl_means_filter
from .skimage_filter import fangkuang_filter, gaussian_filter, average_filter, laplace_filter, prewitt_filter, scharr_filter, sobel_filter

__all__ = ["average_filter", "gaussian_filter", "median_filter", "bilateral_filter", "Morphological_filter",
           "NLM_filter", "threshAverFilter", "Box_filter", "laplacian_filter", "edge_preserving_filter", "fft_filter",
           "median_filter", "gaussian_filter", "laplace_filter", "blur_filter", "bilateral_filter", "bilateral_funcs",
           "WLS_filter", "nl_means_filter", "fangkuang_filter", "gaussian_filter", "average_filter", "laplace_filter",
           "prewitt_filter", "scharr_filter", "sobel_filter"]

