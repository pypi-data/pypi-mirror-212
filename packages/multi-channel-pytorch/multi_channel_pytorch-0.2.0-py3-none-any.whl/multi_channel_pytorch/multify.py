from torch.nn import Module

from multi_channel_pytorch.injection import *


def multify(model: Module, num_channels: int = 3):
    architecture: str = model.__class__.__name__.lower()

    if architecture == 'densenet' or architecture == 'alexnet':
        model = features_0(model=model, num_channels=num_channels)
    elif architecture == 'convnext' or architecture == 'swintransformer' or architecture == 'efficientnet':
        model = features_0_0(model=model, num_channels=num_channels)
    elif architecture == 'resnet':
        model = conv1(model=model, num_channels=num_channels)
    elif architecture == 'visiontransformer':
        model = conv_proj(model=model, num_channels=num_channels)
    else:
        raise ValueError("Architecture not supported.")

    return model
