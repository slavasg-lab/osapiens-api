import torch
import torch.nn as nn
from PIL import Image
import torchvision.transforms as transforms
import io


#MODEL

def double_conv(input_channels, output_channels):
    return nn.Sequential(
      nn.Conv2d(input_channels, output_channels, kernel_size=(3,3), stride=1, padding=1),
      nn.BatchNorm2d(output_channels),
      nn.ReLU(inplace=True),
      nn.Conv2d(output_channels, output_channels, kernel_size=(3,3), stride=1, padding=1),
      nn.BatchNorm2d(output_channels),
      nn.ReLU(inplace=True)
    )

def up_conv(input_channels, output_channels):
    return nn.Sequential(
      nn.ConvTranspose2d(input_channels, output_channels, kernel_size=(2,2), stride=2),
      nn.BatchNorm2d(output_channels),
      nn.ReLU(inplace=True)
  )

class ForestSegmentation(nn.Module):
    def __init__(self, encoder_channel, decoder_channel, input_channels, bottom_channels, class_number):
        super().__init__()
        self.encoder_channel = encoder_channel
        self.decoder_channel = decoder_channel
        self.bottom_channels = bottom_channels
        self.class_number = class_number

        self.encoder1 = double_conv(input_channels, encoder_channel[0])

        self.encoder2 = nn.Sequential(nn.MaxPool2d(kernel_size=2, stride=2),
                                      double_conv(encoder_channel[0], encoder_channel[1]))

        self.encoder3 = nn.Sequential(nn.MaxPool2d(kernel_size=2, stride=2),
                                      double_conv(encoder_channel[1], encoder_channel[2]))

        self.encoder4 = nn.Sequential(nn.MaxPool2d(kernel_size=2, stride=2),
                                      double_conv(encoder_channel[2], encoder_channel[3]))

        self.bottleneck = nn.Sequential(nn.MaxPool2d(kernel_size=2, stride=2),
                                        double_conv(encoder_channel[3], bottom_channels))

        self.decoder1up = up_conv(bottom_channels, bottom_channels)
        self.decoder1 = double_conv(encoder_channel[3]+bottom_channels, decoder_channel[0])

        self.decoder2up = up_conv(decoder_channel[0], decoder_channel[0])
        self.decoder2 = double_conv(encoder_channel[2]+decoder_channel[0], decoder_channel[1])

        self.decoder3up = up_conv(decoder_channel[1], decoder_channel[1])
        self.decoder3 = double_conv(encoder_channel[1]+decoder_channel[1], decoder_channel[2])

        self.decoder4up = up_conv(decoder_channel[2], decoder_channel[2])
        self.decoder4 = double_conv(encoder_channel[0]+decoder_channel[2], decoder_channel[3])

        self.classifier = nn.Conv2d(decoder_channel[3], class_number, kernel_size=(1,1))

    def forward(self, x):

        # Encoder
        encoder1 = self.encoder1(x)
        encoder2 = self.encoder2(encoder1)
        encoder3 = self.encoder3(encoder2)
        encoder4 = self.encoder4(encoder3)

        # Bottleneck
        x = self.bottleneck(encoder4)

        # Decoder
        x = self.decoder1up(x)
        x = torch.concat([x, encoder4], dim=1)
        x = self.decoder1(x)

        x = self.decoder2up(x)
        x = torch.concat([x, encoder3], dim=1)
        x = self.decoder2(x)

        x = self.decoder3up(x)
        x = torch.concat([x, encoder2], dim=1)
        x = self.decoder3(x)

        x = self.decoder4up(x)
        x = torch.concat([x, encoder1], dim=1)
        x = self.decoder4(x)

        # Classifier head
        x = self.classifier(x)

        return x
    


# CREATE MODEL SINGLETONE 
# model = ForestSegmentation(encoder_channel=[16,32,64,128], 
#                              decoder_channel=[128,64,32,16], 
#                              input_channels=3, 
#                              bottom_channels=256, 
#                              class_number=2)

# DEVICE = 'cuda' if torch.cuda.is_available else 'cpu'

# best_weight = torch.load('./rgb_forest_segmentation_model_0.9076792001724243_iou.pt', map_location=DEVICE)
# model.load_state_dict(best_weight)

# # PLACE INTO API CALL

# # Path to your image
# image_path = './dataset/map-screenshot(23).png'

# # Load the image
# image = Image.open(image_path)

