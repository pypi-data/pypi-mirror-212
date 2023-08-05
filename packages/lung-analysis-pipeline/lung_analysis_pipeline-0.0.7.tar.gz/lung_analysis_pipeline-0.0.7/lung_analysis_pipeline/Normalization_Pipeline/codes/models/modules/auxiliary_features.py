import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models
# from torchvision.models.feature_extraction import create_feature_extractor
from torchvision import transforms


class VGGContentLoss(nn.Module):
    """
    Constructs a content loss function based on the VGG19 network.
    Using high-level feature mapping layers from the latter layers will focus more on the texture content of the image.
    Paper reference list:
        -`Photo-Realistic Single Image Super-Resolution Using a Generative Adversarial Network <https://arxiv.org/pdf/1609.04802.pdf>` paper.
        -`ESRGAN: Enhanced Super-Resolution Generative Adversarial Networks                    <https://arxiv.org/pdf/1809.00219.pdf>` paper.
        -`Perceptual Extreme Super Resolution Network with Receptive Field Block               <https://arxiv.org/pdf/2005.12597.pdf>` paper.
     """
    def __init__(self, feature_model_extractor_node: str,
                 feature_model_normalize_mean: list,
                 feature_model_normalize_std: list):
        super(VGGContentLoss, self).__init__()
        self.feature_model_extractor_node = feature_model_extractor_node
        model = models.vgg19(True)
        # Extract the thirty-fifth layer output in the VGG19 model as the content loss.
        self.feature_extractor = create_feature_extractor(model, [feature_model_extractor_node])
        # set to validation mode
        self.feature_extractor.eval()
        self.normalize = transforms.Normalize(feature_model_normalize_mean, feature_model_normalize_std)
        # Freeze model parameters
        for model_parameters in self.feature_extractor.parameters():
            model_parameters.requires_grad = False

    def forward(self, sr_tensor: torch.Tensor, hr_tensor: torch.Tensor) -> torch.Tensor:
        # print('Inside `ContentLoss` forward function')
        # Standardized operations
        # print('BeforeNorm - SR min-max:', sr_tensor.min(), sr_tensor.max())
        # print('BeforeNorm - HR min-max:', hr_tensor.min(), hr_tensor.max())
        sr_tensor = self.normalize(sr_tensor) # 0 to 1 (before norm) | -2 to 2 (after norm)
        hr_tensor = self.normalize(hr_tensor)

        # print('AfterNorm - SR min-max:', sr_tensor.min(), sr_tensor.max())
        # print('AfterNorm - HR min-max:', hr_tensor.min(), hr_tensor.max())

        sr_feature = self.feature_extractor(sr_tensor)[self.feature_model_extractor_node]
        hr_feature = self.feature_extractor(hr_tensor)[self.feature_model_extractor_node]

        # Find the feature map difference between the two images
        content_loss = F.l1_loss(sr_feature, hr_feature)
        return content_loss











"""
Perceptual Network - Assume input range is [0, 1]
"""
"""
class VGGFeatureExtractor(nn.Module):
    def __init__(self,
                 feature_layer=34,
                 use_bn=False,
                 use_input_norm=True, # normalizes input tensor before feeding to model
                 device=torch.device('cpu')):
        super(VGGFeatureExtractor, self).__init__()
        # if 'use_bn'=True; initialize vgg19 with batchnorm
        if use_bn:
            model = torchvision.models.vgg19_bn(pretrained=True)
        else:
            # if 'use_bn'=True; initialize vgg19 without batchnorm
            model = torchvision.models.vgg19(pretrained=True)
        
        self.use_input_norm = use_input_norm
        if self.use_input_norm:
            # define 'mean' and 'std' variable (for normalization) of size similar to input data
            mean = torch.Tensor([0.485, 0.456, 0.406]).view(1, 3, 1, 1).to(device)
            # [0.485-1, 0.456-1, 0.406-1] if input in range [-1,1]
            std = torch.Tensor([0.229, 0.224, 0.225]).view(1, 3, 1, 1).to(device)
            # [0.229*2, 0.224*2, 0.225*2] if input in range [-1,1]

            # creates 'self.mean' and 'self.std' attribute with value defined by above 'mean' and 'std'
            self.register_buffer('mean', mean)
            self.register_buffer('std', std)
        
        # unpack modules in 'nn.Sequential' upto the defined 'feature_layer' before activation
        self.features = nn.Sequential(*list(model.features.children())[:(feature_layer + 1)])
        
        # No need to Back Propogate the parameters, so we set 'require_grad' to False
        for k, v in self.features.named_parameters():
            v.requires_grad = False

    def forward(self, x):
        # if 'self.use_input_norm' is True, normalize data by 'self.mean' and 'self.std'
        if self.use_input_norm:
            x = (x - self.mean) / self.std
        # get output and return
        output = self.features(x)
        return output
"""

class MINCNet(nn.Module):
    def __init__(self):
        super(MINCNet, self).__init__()
        self.ReLU = nn.ReLU(True)
        self.conv11 = nn.Conv2d(3, 64, 3, 1, 1)
        self.conv12 = nn.Conv2d(64, 64, 3, 1, 1)
        self.maxpool1 = nn.MaxPool2d(2, stride=2, padding=0, ceil_mode=True)
        self.conv21 = nn.Conv2d(64, 128, 3, 1, 1)
        self.conv22 = nn.Conv2d(128, 128, 3, 1, 1)
        self.maxpool2 = nn.MaxPool2d(2, stride=2, padding=0, ceil_mode=True)
        self.conv31 = nn.Conv2d(128, 256, 3, 1, 1)
        self.conv32 = nn.Conv2d(256, 256, 3, 1, 1)
        self.conv33 = nn.Conv2d(256, 256, 3, 1, 1)
        self.maxpool3 = nn.MaxPool2d(2, stride=2, padding=0, ceil_mode=True)
        self.conv41 = nn.Conv2d(256, 512, 3, 1, 1)
        self.conv42 = nn.Conv2d(512, 512, 3, 1, 1)
        self.conv43 = nn.Conv2d(512, 512, 3, 1, 1)
        self.maxpool4 = nn.MaxPool2d(2, stride=2, padding=0, ceil_mode=True)
        self.conv51 = nn.Conv2d(512, 512, 3, 1, 1)
        self.conv52 = nn.Conv2d(512, 512, 3, 1, 1)
        self.conv53 = nn.Conv2d(512, 512, 3, 1, 1)

    def forward(self, x):
        out = self.ReLU(self.conv11(x))
        out = self.ReLU(self.conv12(out))
        out = self.maxpool1(out)
        out = self.ReLU(self.conv21(out))
        out = self.ReLU(self.conv22(out))
        out = self.maxpool2(out)
        out = self.ReLU(self.conv31(out))
        out = self.ReLU(self.conv32(out))
        out = self.ReLU(self.conv33(out))
        out = self.maxpool3(out)
        out = self.ReLU(self.conv41(out))
        out = self.ReLU(self.conv42(out))
        out = self.ReLU(self.conv43(out))
        out = self.maxpool4(out)
        out = self.ReLU(self.conv51(out))
        out = self.ReLU(self.conv52(out))
        out = self.conv53(out)
        return out


# Assume input range is [0, 1]
class MINCFeatureExtractor(nn.Module):
    def __init__(self, feature_layer=34, use_bn=False, use_input_norm=True, \
                device=torch.device('cpu')):
        super(MINCFeatureExtractor, self).__init__()

        self.features = MINCNet()
        self.features.load_state_dict(
            torch.load('../experiments/pretrained_models/VGG16minc_53.pth'), strict=True)
        self.features.eval()
        # No need to BP to variable
        for k, v in self.features.named_parameters():
            v.requires_grad = False

    def forward(self, x):
        output = self.features(x)
        return output
