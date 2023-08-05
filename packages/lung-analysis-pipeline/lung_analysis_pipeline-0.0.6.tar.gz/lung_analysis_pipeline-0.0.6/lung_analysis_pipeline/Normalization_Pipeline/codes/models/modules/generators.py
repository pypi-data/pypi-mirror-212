import torch.nn as nn
import torch
import torch.nn.functional as F
from . import block as B
from .bam import *


"""
SR-ResNet Architecture with Continuous Attention to Candidates
"""
class Conditioned_SRResNet_WithCand_Attenv2(nn.Module):
    # in_nc=1, out_nc=1, nf=64, nb=8, upscale=1, norm_type=None, act_type='relu' 
    def __init__(self, in_nc, out_nc, nf, nb, kernel_class, dose_class, upscale=1, norm_type='batch', act_type='relu'):
        super(Conditioned_SRResNet_WithCand_Attenv2, self).__init__()

        # label embeddings
        self.gen_kernel_embedding = nn.Sequential(nn.Embedding(kernel_class, kernel_class), nn.Linear(kernel_class, 32*64*64))
        self.gen_dose_embedding = nn.Sequential(nn.Embedding(dose_class, dose_class), nn.Linear(dose_class, 32*64*64))

        # head-block
        """
        Conv3d(1, 64, kernel_size=(3, 3, 3), stride=(1, 1, 1), padding=(1, 1, 1))
        """
        self.head_conv = nn.Conv3d(in_nc+2, nf, 3, 1, 1, bias=True)
        self.merge_cand = nn.quantized.FloatFunctional()
        
        # body-block: create resnet blocks depending on 'nb' parameters, with attention modules
        attention_blocks = [BAM(nf) for _ in range(nb)]
        self.attn_blocks = nn.Sequential(*attention_blocks)
        resnet_blocks = [ResNetBlock(nf, nf, kernel_size=3, act_type=act_type) for _ in range(nb)]
        # self.net = B.sequential(B.ShortcutBlock(B.sequential(*resnet_blocks, lr_conv)))
        self.net = nn.Sequential(*resnet_blocks)
        self.final_residual = B.conv_block(nf, nf, kernel_size=3, norm_type=norm_type, act_type=None)

        # tail-block
        self.hr_conv = B.conv_block(nf, nf, kernel_size=3, norm_type=norm_type, act_type=act_type)
        self.last_conv = nn.Conv3d(nf, out_nc, 3, 1, 1, bias=True)

    def forward(self, x, gen_kernel_lbl, gen_dose_lbl, candidates):
        # pass through label embeddings
        gen_kernel_embed = self.gen_kernel_embedding(gen_kernel_lbl).view(-1, x.shape[1], x.shape[2], x.shape[3], x.shape[4])
        gen_dose_embed = self.gen_dose_embedding(gen_dose_lbl).view(-1, x.shape[1], x.shape[2], x.shape[3], x.shape[4])
        # add embedding to image and candidate
        x = torch.cat((x, gen_kernel_embed, gen_dose_embed), dim=1)
        x_cand = torch.cat((candidates, gen_kernel_embed, gen_dose_embed), dim=1)
        # pass image and candidate through head-block
        x = self.head_conv(x)
        reuse_head = x.clone() # resuse after residual blocks
        x_cand = self.head_conv(x_cand)
        # x_with_cand = self.merge_cand.add(x, x_cand) # add image with candidates
        # pass through body block
        for _ in range(len(self.net)):
            x_cand = self.attn_blocks[_](x_cand)
            x = self.net[_](x)
            x = self.merge_cand.add(x, x_cand)
        x = self.merge_cand.add(reuse_head, self.final_residual(x))
        # pass through tail block
        x = self.hr_conv(x)
        x = self.last_conv(x)
        return x


"""
SR-ResNet Architecture with Attention to Candidates
"""
class Conditioned_SRResNet_WithCand_Atten(nn.Module):
    # in_nc=1, out_nc=1, nf=64, nb=8, upscale=1, norm_type=None, act_type='relu' 
    def __init__(self, in_nc, out_nc, nf, nb, kernel_class, dose_class, upscale=1, norm_type='batch', act_type='relu'):
        super(Conditioned_SRResNet_WithCand_Atten, self).__init__()

        # label embeddings
        self.gen_kernel_embedding = nn.Sequential(nn.Embedding(kernel_class, kernel_class), nn.Linear(kernel_class, 32*64*64))
        self.gen_dose_embedding = nn.Sequential(nn.Embedding(dose_class, dose_class), nn.Linear(dose_class, 32*64*64))

        # head
        """
        Conv3d(1, 64, kernel_size=(3, 3, 3), stride=(1, 1, 1), padding=(1, 1, 1))
        """
        self.head_conv = nn.Conv3d(in_nc+2, nf, 3, 1, 1, bias=True)
        self.merge_cand = nn.quantized.FloatFunctional()
        
        # body: create a number of resnet blocks depending on 'nb' parameters, with attention modules
        attention = [BAM(nf) for _ in range(nb)]
        resnet_blocks = [ResNetBlockWithAtten(nf, nf, atten_module=attention[_], kernel_size=3, act_type=act_type) for _ in range(nb)]
        # body: after end of all residual blocks
        lr_conv = B.conv_block(nf, nf, kernel_size=3, norm_type=norm_type, act_type=None)

        # The 'up' and 'up_conv' are only used when 'upscale' is not 1. i.e used only for SR 
        # upsample (scale factor is Depth, Height, Width). For upsampling depth, factor comes from config file
        up = nn.Upsample(scale_factor=(upscale, 1., 1.,), mode='nearest')
        up_conv = B.conv_block(nf, nf, kernel_size=3, norm_type=norm_type, act_type=act_type)
        
        # tail
        hr_conv = B.conv_block(nf, nf, kernel_size=3, norm_type=norm_type, act_type=act_type)
        last_conv = nn.Conv3d(nf, out_nc, 3, 1, 1, bias=True)

        # unpack all above defined layers, e.g. 'fea_conv', 'hr_conv', ..., into one 'nn.Sequential' module
        if upscale == 1: # denoising
            self.net = B.sequential(B.ShortcutBlock(B.sequential(*resnet_blocks, lr_conv)), hr_conv, last_conv)
        else: # super-res
            self.net = B.sequential(B.ShortcutBlock(B.sequential(*resnet_blocks, lr_conv)),
                                    up, up_conv, hr_conv, last_conv)

    def forward(self, x, gen_kernel_lbl, gen_dose_lbl, candidates):
        gen_kernel_embed = self.gen_kernel_embedding(gen_kernel_lbl).view(-1, x.shape[1], x.shape[2], x.shape[3], x.shape[4])
        gen_dose_embed = self.gen_dose_embedding(gen_dose_lbl).view(-1, x.shape[1], x.shape[2], x.shape[3], x.shape[4])
        # add embedding to image and candidate
        x = torch.cat((x, gen_kernel_embed, gen_dose_embed), dim=1)
        x_cand = torch.cat((candidates, gen_kernel_embed, gen_dose_embed), dim=1)
        # pass through head
        x = self.head_conv(x)
        x_cand = self.head_conv(x_cand)
        x_with_can = self.merge_cand.add(x, x_cand)
        x = self.net(x_with_can)
        return x


"""
SR-ResNet Architecture with Label Encoding 
"""
class Conditioned_SRResNet(nn.Module):
    # in_nc=1, out_nc=1, nf=64, nb=8, upscale=1, norm_type=None, act_type='relu' 
    def __init__(self, in_nc, out_nc, nf, nb, kernel_class, dose_class, upscale=1, norm_type='batch', act_type='relu', atten_lyrs=False):
        super(Conditioned_SRResNet, self).__init__()

        # label embeddings
        self.gen_kernel_embedding = nn.Sequential(nn.Embedding(kernel_class, kernel_class), nn.Linear(kernel_class, 32*64*64))
        self.gen_dose_embedding = nn.Sequential(nn.Embedding(dose_class, dose_class), nn.Linear(dose_class, 32*64*64))

        # head
        """
        Conv3d(1, 64, kernel_size=(3, 3, 3), stride=(1, 1, 1), padding=(1, 1, 1))
        """
        fea_conv = nn.Conv3d(in_nc+2, nf, 3, 1, 1, bias=True)
        
        # body: create a number of resnet blocks depending on 'nb' parameters
        if atten_lyrs:
            attention = [BAM(nf) for _ in range(nb)]
            resnet_blocks = [ResNetBlockWithAtten(nf, nf, atten_module=attention[_], kernel_size=3, act_type=act_type) for _ in range(nb)]
        else:
            resnet_blocks = [ResNetBlock(nf, nf, kernel_size=3, act_type=act_type) for _ in range(nb)]
        # body: after end of all residual blocks
        lr_conv = B.conv_block(nf, nf, kernel_size=3, norm_type=norm_type, act_type=None)

        # The 'up' and 'up_conv' are only used when 'upscale' is not 1. i.e used only for SR 
        # upsample (scale factor is Depth, Height, Width). For upsampling depth, factor comes from config file
        up = nn.Upsample(scale_factor=(upscale, 1., 1.,), mode='nearest')
        # print("up:", up)
        up_conv = B.conv_block(nf, nf, kernel_size=3, norm_type=norm_type, act_type=act_type)
        # print("up-conv:", up_conv)
        
        # tail
        hr_conv = B.conv_block(nf, nf, kernel_size=3, norm_type=norm_type, act_type=act_type)
        # print("hr conv:", hr_conv)
        last_conv = nn.Conv3d(nf, out_nc, 3, 1, 1, bias=True)
        # print("last conv:", last_conv)

        # unpack all above defined layers, e.g. 'fea_conv', 'hr_conv', ..., into one 'nn.Sequential' module
        if upscale == 1: # denoising
            self.net = B.sequential(fea_conv, B.ShortcutBlock(B.sequential(*resnet_blocks, lr_conv)), hr_conv, last_conv)
        else: # super-res
            self.net = B.sequential(fea_conv, B.ShortcutBlock(B.sequential(*resnet_blocks, lr_conv)),
                                    up, up_conv, hr_conv, last_conv)

    def forward(self, x, gen_kernel_lbl, gen_dose_lbl):
        gen_kernel_embed = self.gen_kernel_embedding(gen_kernel_lbl).view(-1, x.shape[1], x.shape[2], x.shape[3], x.shape[4])
        gen_dose_embed = self.gen_dose_embedding(gen_dose_lbl).view(-1, x.shape[1], x.shape[2], x.shape[3], x.shape[4])
        x = torch.cat((x, gen_kernel_embed, gen_dose_embed), dim=1)
        x = self.net(x)
        return x


"""
SR-ResNet Architecture
"""
class SRResNet(nn.Module):
    # in_nc=1, out_nc=1, nf=64, nb=8, upscale=1, norm_type=None, act_type='relu' 
    def __init__(self, in_nc, out_nc, nf, nb, upscale=1, norm_type='batch', act_type='relu'):
        super(SRResNet, self).__init__()
        # head
        """
        Conv3d(1, 64, kernel_size=(3, 3, 3), stride=(1, 1, 1), padding=(1, 1, 1))
        """
        fea_conv = nn.Conv3d(in_nc, nf, 3, 1, 1, bias=True)
        # print("feature 1:", fea_conv)

        # body: create a number of resnet blocks depending on 'nb' parameters
        resnet_blocks = [ResNetBlock(nf, nf, 3, act_type=act_type) for _ in range(nb)]
        # body: after end of all residual blocks
        lr_conv = B.conv_block(nf, nf, kernel_size=3, norm_type=norm_type, act_type=None)
        # print("lr conv:", lr_conv)

        # The 'up' and 'up_conv' are only used when 'upscale' is not 1. i.e used only for SR 
        # upsample (scale factor is Depth, Height, Width). For upsampling depth, factor comes from config file
        up = nn.Upsample(scale_factor=(upscale, 1., 1.,), mode='nearest')
        # print("up:", up)
        up_conv = B.conv_block(nf, nf, kernel_size=3, norm_type=norm_type, act_type=act_type)
        # print("up-conv:", up_conv)

        # tail
        hr_conv = B.conv_block(nf, nf, kernel_size=3, norm_type=norm_type, act_type=act_type)
        # print("hr conv:", hr_conv)
        last_conv = nn.Conv3d(nf, out_nc, 3, 1, 1, bias=True)
        # print("last conv:", last_conv)

        # unpack all above defined layers, e.g. 'fea_conv', 'hr_conv', ..., into one 'nn.Sequential' module
        if upscale == 1:# denoising
            self.net = B.sequential(fea_conv, B.ShortcutBlock(B.sequential(*resnet_blocks, lr_conv)),
                                    hr_conv, last_conv)
        else: # super-res
            self.net = B.sequential(fea_conv, B.ShortcutBlock(B.sequential(*resnet_blocks, lr_conv)),
                                    up, up_conv, hr_conv, last_conv)
        """
        # initiazlie kaiming normal
        for key in self.state_dict():
            if key.split('.')[-1]=="weight":
                if "conv" in key:
                    # init.kaiming_normal(self.state_dict()[key], mode='fan_out')
                    init.kaiming_normal_(self.state_dict()[key], mode='fan_out')
                if "bn" in key:
                    if "SpatialGate" in key:
                        self.state_dict()[key][...] = 0
                    else:
                        self.state_dict()[key][...] = 1
            elif key.split(".")[-1]=='bias':
                self.state_dict()[key][...] = 0
        """

    def forward(self, x):
        return self.net(x)


class QuantizedModel(nn.Module):
    # https://leimao.github.io/blog/PyTorch-Static-Quantization/
    def __init__(self, model_fp32):
        super(QuantizedModel, self).__init__()
        # QuantStub converts tensors from floating point to quantized.
        # This will only be used for inputs.
        self.quant = torch.quantization.QuantStub()
        # DeQuantStub converts tensors from quantized to floating point.
        # This will only be used for outputs.
        self.dequant = torch.quantization.DeQuantStub()
        # FP32 model
        self.model_fp32 = model_fp32

    def forward(self, x):
        # manually specify where tensors will be converted from floating
        # point to quantized in the quantized model
        x = self.quant(x)
        x = self.model_fp32(x)
        # manually specify where tensors will be converted from quantized
        # to floating point in the quantized model
        x = self.dequant(x)
        return x


# WGAN paper  https://arxiv.org/abs/1708.00961 only for denoising
# Low Dose CT Image Denoising Using a Generative Adversarial Network with Wasserstein Distance
# and Perceptual Loss
class VanillaNet(nn.Module):
    def __init__(self, in_nc, out_nc, nf, nb):
        super(VanillaNet, self).__init__()
        layers = [nn.Conv3d(in_nc, nf, 3, 1, 1), nn.ReLU()]
        for _ in range(2, nb):
            layers.extend([nn.Conv3d(nf, nf, 3, 1, 1), nn.ReLU()])
        layers.extend([nn.Conv3d(nf, out_nc, 3, 1, 1)]) # removed ReLU layer for stability
        self.net = nn.Sequential(*layers)

    def forward(self, x):
        out = self.net(x)
        return out


class ResNetBlock(nn.Module):
    '''
    ResNet Block, 3-3 style
    with extra residual scaling used in EDSR
    (Enhanced Deep Residual Networks for Single Image Super-Resolution, CVPRW 17)
    '''
    # in_nc=64, out_nc=64, act_type='relu', norm_type=None 
    def __init__(self, in_nc, out_nc, kernel_size=3, stride=1, dilation=1, bias=True, \
                 norm_type=None, act_type='relu', res_scale=1):
        super(ResNetBlock, self).__init__()
        """
        conv0 -> Sequential(
        (0): Conv3d(64, 64, kernel_size=(3, 3, 3), stride=(1, 1, 1), padding=(1, 1, 1))
        (1): ReLU(inplace=True)
        )
        """
        # has activation layer
        conv0 = B.conv_block(in_nc, out_nc, kernel_size, stride, dilation, bias, norm_type, act_type)
        """
        conv1 -> Sequential(
        (0): Conv3d(64, 64, kernel_size=(3, 3, 3), stride=(1, 1, 1), padding=(1, 1, 1))
        )
        """
        # does not have activation layer
        conv1 = B.conv_block(out_nc, out_nc, kernel_size, stride, dilation, bias, norm_type, None)
        """
        self.res -> Sequential(
        (0): Conv3d(64, 64, kernel_size=(3, 3, 3), stride=(1, 1, 1), padding=(1, 1, 1))
        (1): ReLU(inplace=True)
        (2): Conv3d(64, 64, kernel_size=(3, 3, 3), stride=(1, 1, 1), padding=(1, 1, 1))
        )
        """
        self.res = B.sequential(conv0, conv1)
        self.res_scale = res_scale
        """
        Use 'torch.nn.quantized.FloatFunctional' to wrap tensor operations that require special handling 
        for quantization into modules. 
        - Examples are operations like 'add' and 'cat' which require special handling to determine 
        output quantization parameters.
        """
        self.skip_op = nn.quantized.FloatFunctional()
        # print("resnetblock:", self.res)
        # print("skip:", self.skip_op)


    def forward(self, x):
        # multiply residual of x 'self.res(x)' with a scalar factor 'self.res_scale'
        res = self.skip_op.mul_scalar(self.res(x), self.res_scale)
        # return addition of original input 'x' with its residual 'res'
        return self.skip_op.add(x, res)


"""
class ResNetBlockWithCandAtten(nn.Module):
    # in_nc=64, out_nc=64, act_type='relu', norm_type=None 
    def __init__(self, in_nc, out_nc, atten_module, kernel_size=3, stride=1, dilation=1, bias=True, \
                 norm_type=None, act_type='relu', res_scale=1):
        super(ResNetBlockWithCandAtten, self).__init__()
        # has activation layer
        conv0 = B.conv_block(in_nc, out_nc, kernel_size, stride, dilation, bias, norm_type, act_type)
        # does not have activation layer
        conv1 = B.conv_block(out_nc, out_nc, kernel_size, stride, dilation, bias, norm_type, None)
        self.res = B.sequential(conv0, conv1)
        self.res_scale = res_scale
        self.skip_op = nn.quantized.FloatFunctional()
        self.atten_module = atten_module

    def forward(self, x, x_candidate):
        res = self.skip_op.mul_scalar(self.res(x), self.res_scale)
        res = self.skip_op.add(x, res)
        res_with_atten = self.atten_module(res)
        return res_with_atten
"""


class ResNetBlockWithAtten(nn.Module):
    # in_nc=64, out_nc=64, act_type='relu', norm_type=None 
    def __init__(self, in_nc, out_nc, atten_module, kernel_size=3, stride=1, dilation=1, bias=True, \
                 norm_type=None, act_type='relu', res_scale=1):
        super(ResNetBlockWithAtten, self).__init__()
        # has activation layer
        conv0 = B.conv_block(in_nc, out_nc, kernel_size, stride, dilation, bias, norm_type, act_type)
        # does not have activation layer
        conv1 = B.conv_block(out_nc, out_nc, kernel_size, stride, dilation, bias, norm_type, None)
        self.res = B.sequential(conv0, conv1)
        self.res_scale = res_scale
        self.skip_op = nn.quantized.FloatFunctional()
        self.atten_module = atten_module

    def forward(self, x):
        res = self.skip_op.mul_scalar(self.res(x), self.res_scale)
        res = self.skip_op.add(x, res)
        res_with_atten = self.atten_module(res)
        return res_with_atten


####################
# FSRCNN
####################
class FSRCNN(nn.Module):
    def __init__(self, scale_factor=1, num_channels=1, d=56, s=12, m=4):
        super(FSRCNN, self).__init__()
        self.first_part = nn.Sequential(
            nn.Conv3d(num_channels, d, kernel_size=5, padding=5//2),
            nn.PReLU(d)
        )
        self.mid_part = [nn.Conv3d(d, s, kernel_size=1), nn.PReLU(s)]
        for _ in range(m):
            self.mid_part.extend([nn.Conv3d(s, s, kernel_size=3, padding=3//2), nn.PReLU(s)])
        self.mid_part.extend([nn.Conv3d(s, d, kernel_size=1), nn.PReLU(d)])
        self.mid_part = nn.Sequential(*self.mid_part)
        self.last_part = nn.ConvTranspose3d(d, num_channels, kernel_size=(9, 5, 5), stride=(scale_factor, 1, 1), padding=(4, 2, 2),
                                            output_padding=(scale_factor-1, 0, 0))

    def forward(self, x):
        x = self.first_part(x)
        x = self.mid_part(x)
        return self.last_part(x)


####################
# SLResNet
####################
class SLResNet(nn.Module):
    def __init__(self, in_nc, out_nc, nf, nb, inter_nc, upscale=1, norm_type='batch', act_type='relu'):
        super(SLResNet, self).__init__()

        # feature extraction/ denoise
        # fea_conv = B.conv_block(in_nc, nf, kernel_size=3, norm_type=norm_type, act_type=act_type)
        fea_conv = nn.Conv3d(in_nc, nf, kernel_size=5, padding=5//2, bias=True)
        resnet_blocks = [SL_A_ResNetBlock(nf, nf, inter_nc, 3, act_type=act_type) for _ in range(nb)]
        lr_conv = B.conv_block(nf, nf, kernel_size=3, norm_type=norm_type, act_type=None)
        # upsample 
        up = nn.Upsample(scale_factor=(upscale, 1., 1.,), mode='nearest')
        up_conv = B.conv_block(nf, nf, kernel_size=3, norm_type=norm_type, act_type=act_type)
        # output
        hr_conv = B.conv_block(nf, nf, kernel_size=3, norm_type=norm_type, act_type=act_type)
        conv_last = nn.Conv3d(nf, out_nc, 3, 1, 1, bias=True)

        if upscale == 1:# denoising
            self.net = B.sequential(fea_conv, B.ShortcutBlock(B.sequential(*resnet_blocks, lr_conv)),
                    hr_conv, conv_last)
        else: #super-res
            self.net = B.sequential(fea_conv, B.ShortcutBlock(B.sequential(*resnet_blocks, lr_conv)),
                                up, up_conv, hr_conv, conv_last)

    def forward(self, x):
        return self.net(x)

class SL_A_ResNetBlock(nn.Module):
    def __init__(self, in_nc, out_nc, inter_nc, kernel_size=3, stride=1, dilation=1, bias=True, \
                 norm_type=None, act_type='relu'):
        super(SL_A_ResNetBlock, self).__init__()
        spa_conv = B.s_conv_block(in_nc, inter_nc, kernel_size, stride, dilation, bias, norm_type, act_type)
        temp_conv = B.t_conv_block(inter_nc, out_nc, kernel_size, stride, dilation, bias, norm_type, None)
        self.res = B.sequential(spa_conv, temp_conv)
        self.skip_op = nn.quantized.FloatFunctional()

    def forward(self, x):
        return self.skip_op.add(x, self.res(x))

class SL_B_ResNetBlock(nn.Module):
    def __init__(self, in_nc, out_nc, bk_nc, inter_nc, kernel_size=3, stride=1, dilation=1, bias=True, \
                 norm_type=None, act_type='relu'):
        super(SL_B_ResNetBlock, self).__init__()

        self.spa_conv = B.s_conv_block(in_nc, inter_nc, kernel_size, stride, dilation, bias, norm_type, act_type)
        self.temp_conv = B.t_conv_block(in_nc, inter_nc, kernel_size, stride, dilation, bias, norm_type, act_type)
        self.conv1 = B.conv_block(inter_nc, out_nc, 1, stride, dilation, bias, norm_type, None)
        self.is_not_out_nc_equal_to_inter_nc = out_nc != inter_nc

    def forward(self, x):
        out = self.spa_conv(x) + self.temp_conv(x) # parallel spatial temporal
        if self.is_not_out_nc_equal_to_inter_nc:
            out = self.conv1(out) # 1x1x1 conv when out_nc != inter_nc
        return x + out

class SL_C_ResNetBlock(nn.Module):
    def __init__(self, in_nc, out_nc, bk_nc, inter_nc, kernel_size=3, stride=1, dilation=1, bias=True, \
                 norm_type=None, act_type='relu'):
        super(SL_C_ResNetBlock, self).__init__()

        self.spa_conv = B.s_conv_block(in_nc, inter_nc, kernel_size, stride, dilation, bias, norm_type, act_type)
        self.temp_conv = B.t_conv_block(inter_nc, inter_nc, kernel_size, stride, dilation, bias, norm_type, act_type)
        self.conv1 = B.conv_block(inter_nc, out_nc, 1, stride, dilation, bias, norm_type, None)

        self.is_not_out_nc_equal_to_inter_nc = out_nc != inter_nc

    def forward(self, x):
        out = self.spa_conv(x) 
        out = out + self.temp_conv(out) # fuse spatial & temporal
        if self.is_not_out_nc_equal_to_inter_nc:
            out = self.conv1(out) # 1x1x1 conv when out_nc != inter_nc
        return x + out


"""
Dense block for RRBD MODEL
"""
class ResidualDenseBlock(nn.Module):
    """Achieves densely connected convolutional layers.
    `Densely Connected Convolutional Networks <https://arxiv.org/pdf/1608.06993v5.pdf>` paper.

    Args:
        channels (int): The number of channels in the input image.
        growth_channels (int): The number of channels that increase in each layer of convolution.
    """
    def __init__(self, channels: int, growth_channels: int) -> None:
        super(ResidualDenseBlock, self).__init__()
        self.conv1 = nn.Conv3d(channels + growth_channels * 0, growth_channels, (3, 3, 3), (1, 1, 1), (1, 1, 1))
        self.conv2 = nn.Conv3d(channels + growth_channels * 1, growth_channels, (3, 3, 3), (1, 1, 1), (1, 1, 1))
        self.conv3 = nn.Conv3d(channels + growth_channels * 2, growth_channels, (3, 3, 3), (1, 1, 1), (1, 1, 1))
        self.conv4 = nn.Conv3d(channels + growth_channels * 3, growth_channels, (3, 3, 3), (1, 1, 1), (1, 1, 1))
        self.conv5 = nn.Conv3d(channels + growth_channels * 4, channels, (3, 3, 3), (1, 1, 1), (1, 1, 1))
        self.leaky_relu = nn.LeakyReLU(0.2, True)
        self.identity = nn.Identity()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        identity = x
        out1 = self.leaky_relu(self.conv1(x))
        out2 = self.leaky_relu(self.conv2(torch.cat([x, out1], 1)))
        out3 = self.leaky_relu(self.conv3(torch.cat([x, out1, out2], 1)))
        out4 = self.leaky_relu(self.conv4(torch.cat([x, out1, out2, out3], 1)))
        out5 = self.identity(self.conv5(torch.cat([x, out1, out2, out3, out4], 1)))
        out = torch.mul(out5, 0.2)
        out = torch.add(out, identity)
        return out


class ResidualResidualDenseBlock(nn.Module):
    """Multi-layer residual dense convolution block.
    Args:
        channels (int): The number of channels in the input image.
        growth_channels (int): The number of channels that increase in each layer of convolution.
    """
    def __init__(self, channels: int, growth_channels: int) -> None:
        super(ResidualResidualDenseBlock, self).__init__()
        self.rdb1 = ResidualDenseBlock(channels, growth_channels)
        self.rdb2 = ResidualDenseBlock(channels, growth_channels)
        self.rdb3 = ResidualDenseBlock(channels, growth_channels)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        identity = x
        out = self.rdb1(x)
        out = self.rdb2(out)
        out = self.rdb3(out)
        out = torch.mul(out, 0.2)
        out = torch.add(out, identity)
        return out


"""
RRBD MODEL
"""
class RRDB_Gen(nn.Module):
    def __init__(self, in_nc, out_nc, nf, nb, upscale=1):
        super(RRDB_Gen, self).__init__()
        self.conv1 = nn.Conv3d(in_nc, nf, (3, 3, 3), (1, 1, 1), (1, 1, 1))
        # Feature extraction backbone network
        trunk = []
        for _ in range(nb):
            trunk.append(ResidualResidualDenseBlock(nf, 32))
        self.trunk = nn.Sequential(*trunk)
        self.conv2 = nn.Conv3d(nf, nf, (3, 3, 3), (1, 1, 1), (1, 1, 1))
        # Reconnect a layer of convolution block after upsampling
        self.conv3 = nn.Sequential(
            nn.Conv3d(nf, nf, (3, 3, 3), (1, 1, 1), (1, 1, 1)),
            nn.LeakyReLU(0.2, True)
        )
        # Output layer
        self.conv4 = nn.Conv3d(nf, out_nc, (3, 3, 3), (1, 1, 1), (1, 1, 1))

    def _forward_impl(self, x: torch.Tensor) -> torch.Tensor:
        out1 = self.conv1(x)
        out = self.trunk(out1)
        out2 = self.conv2(out)
        out = torch.add(out1, out2)
        out = self.conv3(out)
        out = self.conv4(out)
        out = torch.clamp_(out, 0.0, 1.0)
        return out

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self._forward_impl(x)




"""
####################
# RRDB
####################
class RRDBNet(nn.Module):
    def __init__(self, in_nc, out_nc, nf, nb, gc=32, upscale=1, norm_type=None):
        super(RRDBNet, self).__init__()
        self.upscale = upscale

        # feature extraction/ denoise
        fea_conv = nn.Conv3d(in_nc, nf, 3, 1, 1, bias=True)
        rb_blocks = [RRDB(nf, gc) for _ in range(nb)]
        LR_conv = B.conv_block(nf, nf, kernel_size=3, norm_type=norm_type, act_type=None)
        self.out_feat = B.sequential(fea_conv, B.ShortcutBlock(B.sequential(*rb_blocks, LR_conv)))
        # upsample x2
        self.upconv = nn.Conv3d(nf, nf, 3, 1, 1, bias=True)
        self.lrelu = nn.LeakyReLU(negative_slope=0.2, inplace=True)
        # output
        self.HR_conv = nn.Conv3d(nf, nf, 3, 1, 1, bias=True)
        self.conv_last = nn.Conv3d(nf, out_nc, 3, 1, 1, bias=True)

    def forward(self, x):
        x = self.out_feat(x)
        if self.upscale == 2:
            x = self.lrelu(self.upconv(F.interpolate(x, scale_factor=(2., 1., 1.), mode='nearest')))
        # out = self.conv_last(x)
        return self.conv_last(self.lrelu(self.HR_conv(x)))


class ResidualDenseBlock_5C(nn.Module):
    '''
    Residual Dense Block
    style: 5 convs
    The core module of paper: (Residual Dense Network for Image Super-Resolution, CVPR 18)
    '''
    def __init__(self, nf, gc, kernel_size=3, stride=1, bias=True,
                 norm_type=None, act_type='leakyrelu'):
        super(ResidualDenseBlock_5C, self).__init__()
        # gc: growth channel, i.e. intermediate channels
        self.conv1 = B.conv_block(nf, gc, kernel_size, stride, bias=bias, \
            norm_type=norm_type, act_type=act_type)
        self.conv2 = B.conv_block(nf+gc, gc, kernel_size, stride, bias=bias, \
            norm_type=norm_type, act_type=act_type)
        self.conv3 = B.conv_block(nf+2*gc, gc, kernel_size, stride, bias=bias, \
            norm_type=norm_type, act_type=act_type)
        self.conv4 = B.conv_block(nf+3*gc, gc, kernel_size, stride, bias=bias, \
            norm_type=norm_type, act_type=act_type)
        self.conv5 = B.conv_block(nf+4*gc, nf, 3, stride, bias=bias, \
            norm_type=norm_type, act_type=None)

    def forward(self, x):
        x1 = self.conv1(x)
        x2 = self.conv2(torch.cat((x, x1), 1))
        x3 = self.conv3(torch.cat((x, x1, x2), 1))
        x4 = self.conv4(torch.cat((x, x1, x2, x3), 1))
        x5 = self.conv5(torch.cat((x, x1, x2, x3, x4), 1))
        return x5 * 0.2 + x


class RRDB(nn.Module):
    '''
    Residual in Residual Dense Block
    (ESRGAN: Enhanced Super-Resolution Generative Adversarial Networks)
    '''
    def __init__(self, nf=64, gc=32):
        super(RRDB, self).__init__()
        self.RDB1 = ResidualDenseBlock_5C(nf, gc)
        self.RDB2 = ResidualDenseBlock_5C(nf, gc)
        self.RDB3 = ResidualDenseBlock_5C(nf, gc)

    def forward(self, x):
        out = self.RDB1(x)
        out = self.RDB2(out)
        out = self.RDB3(out)
        return out * 0.2 + x
"""