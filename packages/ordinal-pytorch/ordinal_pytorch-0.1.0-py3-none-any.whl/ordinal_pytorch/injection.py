import torch

from types import MethodType
from coral_pytorch.layers import CoralLayer

from ordinal_pytorch.forward import coral_forward, coral_forward_swintransformer, coral_forward_densenet, coral_forward_visiontransformer, coral_forward_alexnet


def resnet(model: torch.nn.Module, loss: str, num_classes: int):
    match loss:
        case 'corn':
            model.fc = torch.nn.Linear(in_features=model.fc.in_features, out_features=num_classes - 1)
        case 'coral':
            model.fc = CoralLayer(size_in=model.fc.in_features, num_classes=num_classes)
            model.forward = MethodType(coral_forward, model)
        case 'condor':
            model.fc = torch.nn.Linear(in_features=model.fc.in_features, out_features=num_classes - 1)

    return model


# EfficientNet v1 and EfficientNet v2
def efficientnet(model: torch.nn.Module, loss: str, num_classes: int):
    match loss:
        case 'corn':
            model.classifier[-1] = torch.nn.Linear(in_features=model.classifier[-1].in_features, out_features=num_classes - 1)
        case 'coral':
            model.classifier[-1] = CoralLayer(size_in=model.classifier[-1].in_features, num_classes=num_classes)
            model.forward = MethodType(coral_forward, model)
        case 'condor':
            model.classifier[-1] = torch.nn.Linear(in_features=model.classifier[-1].in_features, out_features=num_classes - 1)

    return model


# SwinTransformer
def swintransformer(model: torch.nn.Module, loss: str, num_classes: int):
    match loss:
        case 'corn':
            model.head = torch.nn.Linear(in_features=model.head.in_features, out_features=num_classes - 1)
        case 'coral':
            model.head = CoralLayer(size_in=model.head.in_features, num_classes=num_classes)
            # TODO: maybe get it to work with renaming the original forward method and then also using coral_forward
            model.forward = MethodType(coral_forward_swintransformer, model)
        case 'condor':
            model.head = torch.nn.Linear(in_features=model.head.in_features, out_features=num_classes - 1)

    return model


def alexnet(model: torch.nn.Module, loss: str, num_classes: int):
    match loss:
        case 'corn':
            model.classifier[-1] = torch.nn.Linear(in_features=model.classifier[-1].in_features, out_features=num_classes - 1)
        case 'coral':
            model.classifier[-1] = CoralLayer(size_in=model.classifier[-1].in_features, num_classes=num_classes)
            # TODO: maybe get it to work with renaming the original forward method and then also using coral_forward
            model.forward = MethodType(coral_forward_alexnet, model)
        case 'condor':
            model.classifier[-1] = torch.nn.Linear(in_features=model.classifier[-1].in_features, out_features=num_classes - 1)

    return model


def convnext(model: torch.nn.Module, loss: str, num_classes: int):
    match loss:
        case 'corn':
            model.classifier[-1] = torch.nn.Linear(in_features=model.classifier[-1].in_features, out_features=num_classes - 1)
        case 'coral':
            model.classifier[-1] = CoralLayer(size_in=model.classifier[-1].in_features, num_classes=num_classes)
            model.forward = MethodType(coral_forward, model)
        case 'condor':
            model.classifier[-1] = torch.nn.Linear(in_features=model.classifier[-1].in_features, out_features=num_classes - 1)

    return model


def densenet(model: torch.nn.Module, loss: str, num_classes: int):
    match loss:
        case 'corn':
            model.classifier = torch.nn.Linear(in_features=model.classifier.in_features, out_features=num_classes - 1)
        case 'coral':
            model.classifier = CoralLayer(size_in=model.classifier.in_features, num_classes=num_classes)
            # TODO: maybe get it to work with renaming the original forward method and then also using coral_forward
            model.forward = MethodType(coral_forward_densenet, model)
        case 'condor':
            model.classifier = torch.nn.Linear(in_features=model.classifier.in_features, out_features=num_classes - 1)

    return model


def visiontransformer(model: torch.nn.Module, loss: str, num_classes: int):
    match loss:
        case 'corn':
            model.heads[-1] = torch.nn.Linear(in_features=model.heads[-1].in_features, out_features=num_classes - 1)
        case 'coral':
            model.heads[-1] = CoralLayer(size_in=model.heads[-1].in_features, num_classes=num_classes)
            # TODO: maybe get it to work with renaming the original forward method and then also using coral_forward
            model.forward = MethodType(coral_forward_visiontransformer, model)
        case 'condor':
            model.heads[-1] = torch.nn.Linear(in_features=model.heads[-1].in_features, out_features=num_classes - 1)

    return model
