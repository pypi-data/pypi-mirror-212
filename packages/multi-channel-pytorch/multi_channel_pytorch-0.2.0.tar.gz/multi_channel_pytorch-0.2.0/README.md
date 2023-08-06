# Multi-Channel-Pytorch
> torch, torchvision, multi-channel-input

This library allows to modify known network architectures (e.g. ResNet or EfficientNet) with only one line 
of code to support additional channels to the already given RGB channels. Even pre-trained neural networks 
like ResNet50 can be used.

## Installing / Getting started

Installation works with pypi.

```shell
pip install multi-channel-pytorch
```

## Features

Currently supported architectures:
* AlexNet
* ConvNeXt
* EfficientNet
* EfficientNetV2
* ResNet
* ResNeXt
* SwinTransformer
* VisionTransformer

## Usage

You can add multi channel functionality to one of the previous mentioned architectures with just one line of
code. 

The following is an example of adding multi-channel support to a pre-trained ResNet50 model:

```python
from multi_channel_pytorch import multify
from torchvision.models import resnet50

# Create a ResNet50 model with pretrained weights.
model = resnet50(weights='DEFAULT')

# Add a fourth channel to the previously created model.
model = multify(model=model, num_channels=4)
```

This adds another channel to the input layer of the ResNet50 model:

```python
# First Conv2d layer before multifying with 3 input channels.
Conv2d(3, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False)

# First Conv2d layer after multifying with 4 input channels.
Conv2d(4, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False)
```

Weights of the first three channels from the pretrained model get copied over. The other channels get
initialized randomly with help of the normal distribution:

```python
# Cloning weights before replacing the first Conv2d layer.
weight = model.conv1.weight.clone()

# Initializing weights randomly of all channels of the new Conv2d layer.
model.conv1.weight[:, 3].data.normal_(0, 0.001)

# Copying weights for the first three channels.
model.conv1.weight[:, :3] = weight
```

## Licensing

The code in this project is licensed under GNU General Public License v3.0.