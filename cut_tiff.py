# coding：utf-8
# Bin GAO

import os
import gdal

# input path
in_path = './test/'
input_filename = 'luhe.tiff'

# output path
out_path = './output/'
output_filename = 'luhe_'

# patch size
tile_size_width = 1024
tile_size_height = 1024


ds = gdal.Open(in_path+input_filename)
band = ds.GetRasterBand(1)
x_size = band.XSize
y_size = band.YSize

for i in range(0, x_size, tile_size_width):
    for j in range(0, y_size, tile_size_height):
        cut = "gdal_translate -of GTIFF -srcwin " + str(i)+ ", " + str(j) + ", " \
              + str(tile_size_width) + ", " + str(tile_size_height) + " " \
              + str(in_path) + str(input_filename) + " " \
              + str(out_path) + str(output_filename) + str(i) + "_" + str(j) + ".tif"
        os.system(cut)
