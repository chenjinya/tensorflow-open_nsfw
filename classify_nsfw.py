#!/usr/bin/env python
import sys
import argparse
import tensorflow as tf

from model import OpenNsfwModel, InputType
from image_utils import create_tensorflow_image_loader
from image_utils import create_yahoo_image_loader

import numpy as np
import utils
import os
# os.environ["TF_CPP_MIN_LOG_LEVEL"]='1' # 这是默认的显示等级，显示所有信息  
# os.environ["TF_CPP_MIN_LOG_LEVEL"]='2' # 只显示 warning 和 Error   
os.environ["TF_CPP_MIN_LOG_LEVEL"] = '3'  # 只显示 Error


IMAGE_LOADER_TENSORFLOW = "tensorflow"
IMAGE_LOADER_YAHOO = "yahoo"


def main(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument("input_file", help="Path to the input image.\
                        Only jpeg images are supported.")

    parser.add_argument("-m", "--model_weights", required=True,
                        help="Path to trained model weights file")

    parser.add_argument("-cb", "--callback", default='',
                        help="Callback Url")

    parser.add_argument("-l", "--image_loader",
                        default=IMAGE_LOADER_YAHOO,
                        help="image loading mechanism",
                        choices=[IMAGE_LOADER_YAHOO, IMAGE_LOADER_TENSORFLOW])

    parser.add_argument("-i", "--input_type",
                        default=InputType.TENSOR.name.lower(),
                        help="input type",
                        choices=[InputType.TENSOR.name.lower(),
                                 InputType.BASE64_JPEG.name.lower()])

    args = parser.parse_args()

    model = OpenNsfwModel()
    current_path = os.getcwd()
    dir_path = '%s/porn_detect_temp' % (current_path)
    if 'http' in args.input_file:
        image_file_path = utils.download(args.input_file, dir_path)
        print("image download to: " + image_file_path)
    else:
        image_file_path = args.input_file
    with tf.compat.v1.Session() as sess:

        input_type = InputType[args.input_type.upper()]
        model.build(weights_path=args.model_weights, input_type=input_type)

        fn_load_image = None

        if input_type == InputType.TENSOR:
            if args.image_loader == IMAGE_LOADER_TENSORFLOW:
                fn_load_image = create_tensorflow_image_loader(
                    tf.Session(graph=tf.Graph()))
            else:
                fn_load_image = create_yahoo_image_loader()
        elif input_type == InputType.BASE64_JPEG:
            import base64
            def fn_load_image(filename): return np.array(
                [base64.urlsafe_b64encode(open(filename, "rb").read())])

        sess.run(tf.compat.v1.global_variables_initializer())

        image = fn_load_image(image_file_path)

        predictions = \
            sess.run(model.predictions,
                     feed_dict={model.input: image})

        print("Results for '{}'".format(args.input_file))
        print(predictions)
        print("\tSFW score:\t{}\n\tNSFW score:\t{}".format(*predictions[0]))
        if '' != args.callback:
            param = {
                'id': 758693,
                'sfw': str(predictions[0][0]), 'nsfw': str(predictions[0][1])
            }
            ret = utils.get(args.callback, param)
            print(ret)
    if 'http' in args.input_file:
        os.remove(image_file_path)


if __name__ == "__main__":
    main(sys.argv)
