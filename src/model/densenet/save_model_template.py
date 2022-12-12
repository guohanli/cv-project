import torch
from torchvision import models

# Make sure to pass `pretrained` as `True` to use the pretrained weights:
model = models.densenet121(pretrained=True)
model_scripted = torch.jit.script(model)  # Export to TorchScript
model_scripted.save('../../../resource/densenet/densenet121.pt')  # Save
