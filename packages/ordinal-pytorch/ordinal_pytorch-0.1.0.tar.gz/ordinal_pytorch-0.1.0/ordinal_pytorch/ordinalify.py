import torch

from ordinal_pytorch.injection import alexnet, convnext, densenet, efficientnet, resnet, swintransformer, visiontransformer

ALLOWED_LOSS = [
    'corn',
    'coral',
    'condor'
]


def ordinalify(model: torch.nn.Module, num_classes: int, loss: str = 'corn') -> torch.nn.Module:
    if loss not in ALLOWED_LOSS:
        raise ValueError(f'{loss} is not a valid loss function.\nConsider one of the following:\n{str(ALLOWED_LOSS)}')

    # Get class name of network
    name = model.__class__.__name__.lower()

    # Get corresponding method from this file
    method = globals()[f'_{name}']

    # Inject model with ordinal functionality
    model = method(model=model, loss=loss, num_classes=num_classes)

    return model
