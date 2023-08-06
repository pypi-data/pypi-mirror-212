import torch

from multi_channel_pytorch.utils import get_bias


def features_0(model: torch.nn.Module, num_channels: int = 3) -> torch.nn.Module:
    # Get state dict with only bias
    state_dict = get_bias(state_dict=model.features[0].state_dict())

    # Clone pretrained weights from model
    weight = model.features[0].weight.clone()

    # Create new Conv2d layer with settings from the Conv2d layer of the given model
    model.features[0] = torch.nn.Conv2d(
        in_channels=num_channels,
        out_channels=model.features[0].out_channels,
        kernel_size=model.features[0].kernel_size,
        stride=model.features[0].stride,
        padding=model.features[0].padding,
        dilation=model.features[0].dilation,
        groups=model.features[0].groups,
        padding_mode=model.features[0].padding_mode
    )

    with torch.no_grad():
        # https://stackoverflow.com/questions/49433936/how-do-i-initialize-weights-in-pytorch
        # Initialize weight randomly with Gaussian
        # nn.init.normal_(model.conv1.weight[:, 3], 0, 0.001)
        model.features[0].weight[:, 3].data.normal_(0, 0.001)

        # Copy weights for rgb channels from pretrained model
        model.features[0].weight[:, :3] = weight

        # Set bias from previous state dict
        model.features[0].load_state_dict(state_dict, strict=False)

    return model


def features_0_0(model: torch.nn.Module, num_channels: int = 3):
    # Get state dict with only bias
    state_dict = get_bias(state_dict=model.features[0][0].state_dict())

    # Clone pretrained weights from model
    weight = model.features[0][0].weight.clone()

    # Create new Conv2d layer with settings from the Conv2d layer of the given model
    model.features[0][0] = torch.nn.Conv2d(
        in_channels=num_channels,
        out_channels=model.features[0][0].out_channels,
        kernel_size=model.features[0][0].kernel_size,
        stride=model.features[0][0].stride,
        padding=model.features[0][0].padding,
        dilation=model.features[0][0].dilation,
        groups=model.features[0][0].groups,
        padding_mode=model.features[0][0].padding_mode
    )

    with torch.no_grad():
        # https://stackoverflow.com/questions/49433936/how-do-i-initialize-weights-in-pytorch
        # Initialize weight randomly with Gaussian
        # nn.init.normal_(model.conv1.weight[:, 3], 0, 0.001)
        model.features[0][0].weight[:, 3].data.normal_(0, 0.001)

        # Copy weights for rgb channels from pretrained model
        model.features[0][0].weight[:, :3] = weight

        # Set bias from previous state dict
        model.features[0][0].load_state_dict(state_dict, strict=False)

    return model


def conv1(model: torch.nn.Module, num_channels: int = 3) -> torch.nn.Module:
    # Get state dict with only bias
    state_dict = get_bias(state_dict=model.conv1.state_dict())

    # Clone pretrained weights from model
    weight = model.conv1.weight.clone()

    # Create new Conv2d layer with settings from the Conv2d layer of the given model
    model.conv1 = torch.nn.Conv2d(
        in_channels=num_channels,
        out_channels=model.conv1.out_channels,
        kernel_size=model.conv1.kernel_size,
        stride=model.conv1.stride,
        padding=model.conv1.padding,
        dilation=model.conv1.dilation,
        groups=model.conv1.groups,
        padding_mode=model.conv1.padding_mode
    )

    with torch.no_grad():
        # https://stackoverflow.com/questions/49433936/how-do-i-initialize-weights-in-pytorch
        # Initialize weight randomly with Gaussian
        # nn.init.normal_(model.conv1.weight[:, 3], 0, 0.001)
        model.conv1.weight[:, 3].data.normal_(0, 0.001)

        # Copy weights for rgb channels from pretrained model
        model.conv1.weight[:, :3] = weight

        # Set bias from previous state dict
        model.conv1.load_state_dict(state_dict, strict=False)

    return model


def conv_proj(model: torch.nn.Module, num_channels: int = 3) -> torch.nn.Module:
    # Get state dict with only bias
    state_dict = get_bias(state_dict=model.conv_proj.state_dict())

    # Clone pretrained weights from model
    weight = model.conv_proj.weight.clone()

    # Create new Conv2d layer with settings from the Conv2d layer of the given model
    model.conv_proj = torch.nn.Conv2d(
        in_channels=num_channels,
        out_channels=model.conv_proj.out_channels,
        kernel_size=model.conv_proj.kernel_size,
        stride=model.conv_proj.stride,
        padding=model.conv_proj.padding,
        dilation=model.conv_proj.dilation,
        groups=model.conv_proj.groups,
        padding_mode=model.conv_proj.padding_mode
    )

    with torch.no_grad():
        # https://stackoverflow.com/questions/49433936/how-do-i-initialize-weights-in-pytorch
        # Initialize weight randomly with Gaussian
        model.conv_proj.weight[:, 3].data.normal_(0, 0.001)

        # Copy weights for rgb channels from pretrained model
        model.conv_proj.weight[:, :3] = weight

        # Set bias from previous state dict
        model.conv_proj.load_state_dict(state_dict, strict=False)

    return model
