import torch


def coral_forward_swintransformer(self, x):
    x = self.features(x)
    x = self.norm(x)
    x = self.permute(x)
    x = self.avgpool(x)
    x = self.flatten(x)
    x = self.head(x)

    return x, torch.sigmoid(x)


def coral_forward_alexnet(self, x):
    x = self.features(x)
    x = self.avgpool(x)
    x = torch.flatten(x, 1)
    x = self.classifier(x)

    return x, torch.sigmoid(x)


def coral_forward_densenet(self, x):
    features = self.features(x)

    out = torch.nn.functional.relu(features, inplace=True)
    out = torch.nn.functional.adaptive_avg_pool2d(out, (1, 1))
    out = torch.flatten(out, 1)
    out = self.classifier(out)

    return out, torch.sigmoid(out)


def coral_forward_visiontransformer(self, x):
    # Reshape and permute the input tensor
    x = self._process_input(x)
    n = x.shape[0]

    # Expand the class token to the full batch
    batch_class_token = self.class_token.expand(n, -1, -1)
    x = torch.cat([batch_class_token, x], dim=1)

    x = self.encoder(x)

    # Classifier "token" as used by standard language architectures
    x = x[:, 0]

    x = self.heads(x)

    return x, torch.sigmoid(x)


def coral_forward(self, x):
    x = self._forward_impl(x)

    return x, torch.sigmoid(x)
