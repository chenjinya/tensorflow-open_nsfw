

# ENV


Description:	CentOS Linux release 7.3.1611 (Core)

Release:	7.3.1611

Python: 3.7.4

# Changelog



1. 运行发现提示 `ValueError: Object arrays cannot be loaded when allow_pickle=False`，在 `model.py` 的 `np.load` 里添加 `allow_pickle=True` 参数。

2. 增加了可以下载远程图片的功能

3. 添加了`callback` 参数，可以将结果回传给API

4. 加入了除JPG之外的图片格式支持。(使用了 pillow 库 `pip install pillow`)

# Tips

0. 运行前

安装  `tensorflow` ，whl列表 https://github.com/lakshayg/tensorflow-build

安装 `skimage`, `python -m pip install scikit-image`

1. 如果遇到 `/lib64/libstdc++.so.6: version 'CXXABI_1.3.8' not found`  的问题，请参考  https://blog.csdn.net/EI__Nino/article/details/100086157
2. 如果遇到 `/lib64/libm.so.6: version 'GLIBC_2.23' not found` 的那问题，请参考 https://blog.csdn.net/EI__Nino/article/details/100094484

遇到问题主要是Tensorflow的问题，主要解决方法就是升级 gcc glibc make (gmake)

经过测试，大概识别一张图需要 7 - 8秒的时间。 ( 4 core 16G)


# Tensorflow Implementation of Yahoo's Open NSFW Model

This repository contains an implementation of [Yahoo's Open NSFW Classifier](https://github.com/yahoo/open_nsfw) rewritten in tensorflow.

The original caffe weights have been extracted using [Caffe to TensorFlow](https://github.com/ethereon/caffe-tensorflow). You can find them at `data/open_nsfw-weights.npy`.

## Prerequisites

All code should be compatible with `Python 3.6` and `Tensorflow 1.x` (tested with 1.12). The model implementation can be found in `model.py`.

### Usage

```
> python classify_nsfw.py -m data/open_nsfw-weights.npy test.jpg

Results for 'test.jpg'
	SFW score:	0.9355766177177429
	NSFW score:	0.06442338228225708
```

__Note:__ Currently only jpeg images are supported.

`classify_nsfw.py` accepts some optional parameters you may want to play around with:

```
usage: classify_nsfw.py [-h] -m MODEL_WEIGHTS [-l {yahoo,tensorflow}]
                        [-t {tensor,base64_jpeg}]
                        input_jpeg_file

positional arguments:
  input_file            Path to the input image. Only jpeg images are
                        supported.

optional arguments:
  -h, --help            show this help message and exit
  -m MODEL_WEIGHTS, --model_weights MODEL_WEIGHTS
                        Path to trained model weights file
  -l {yahoo,tensorflow}, --image_loader {yahoo,tensorflow}
                        image loading mechanism
  -i {tensor,base64_jpeg}, --input_type {tensor,base64_jpeg}
                        input type
```

__-l/--image-loader__

The classification tool supports two different image loading mechanisms. 

* `yahoo` (default) replicates yahoo's original image loading and preprocessing. Use this option if you want the same results as with the original implementation
* `tensorflow` is an image loader which uses tensorflow exclusively (no dependencies on `PIL`, `skimage`, etc.). Tries to replicate the image loading mechanism used by the original caffe implementation, differs a bit though due to different jpeg and resizing implementations. See [this issue](https://github.com/mdietrichstein/tensorflow-open_nsfw/issues/2#issuecomment-346125345) for details.

__Note:__ Classification results may vary depending on the selected image loader!

__-i/--input_type__

Determines if the model internally uses a float tensor (`tensor` - `[None, 224, 224, 3]` - default) or a base64 encoded string tensor (`base64_jpeg` - `[None, ]`) as input. If `base64_jpeg` is used, then the `tensorflow` image loader will be used, regardless of the _-l/--image-loader_ argument.


### Tools

The `tools` folder contains some utility scripts to test the model.

__create_predict_request.py__

Takes an input image and generates a json file suitable for prediction requests to a Open NSFW Model deployed with [Google Cloud ML Engine](https://cloud.google.com/ml-engine/docs/concepts/prediction-overview) (`gcloud ml-engine predict`) or [tensorflow-serving](https://www.tensorflow.org/serving/).


__export_savedmodel.py__

Exports the model using the tensorflow serving export api (`SavedModel`). The export can be used to deploy the model on [Google Cloud ML Engine](https://cloud.google.com/ml-engine/docs/concepts/prediction-overview), [Tensorflow Serving]() or on mobile (haven't tried that one yet).

__export_tflite.py__

Exports the model in [TFLite format](https://www.tensorflow.org/lite/). Use this one if you want to run inference on mobile or IoT devices. Please note that the `base64_jpeg` input type does not work with TFLite since the standard runtime lacks a number of required tensorflow operations.

__export_graph.py__

Exports the tensorflow graph and checkpoint. Freezes and optimizes the graph per default for improved inference and deployment usage (e.g. Android, iOS, etc.). Import the graph with `tf.import_graph_def`.


