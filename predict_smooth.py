import tensorflow as tf
import cv2
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import tifffile as tif

from scipy.ndimage.measurements import label
from smooth_tiled_predictions import predict_img_with_smooth_windowing


if __name__ == '__main__':

    os.environ['CUDA_VISIBLE_DEVICES'] = '1'
    saver = tf.train.import_meta_graph("./models/model.ckpt.meta")
    sess = tf.InteractiveSession()
    saver.restore(sess, "models/model.ckpt")
    X = tf.get_collection("inputs")
    pred = tf.get_collection("outputs")[0]

    # input_img = cv2.imread('./test_data/test_n0013_im.png')
    # input_img = cv2.cvtColor(input_img, cv2.COLOR_BGR2RGB)
    input_img = tif.imread('../testing_data/changshou.tif')


    label_pred = predictions_smooth = predict_img_with_smooth_windowing(
        input_img,
        window_size=512,
        subdivisions=2,  # Minimal amount of overlap for windowing. Must be an even number.
        nb_classes=2,
        pred_func=(
            lambda img: sess.run(pred, feed_dict={X: np.expand_dims(img, 0)})
        )
    )
    label_pred = label_pred[:,:,1]
    label_pred[np.where(label_pred >= 0.5)] = 255
    label_pred[np.where(label_pred < 0.5)] = 0
    cv2.imwrite('./label.png', label_pred)

