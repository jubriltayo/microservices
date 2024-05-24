from django.shortcuts import render
from django.http import HttpResponse
import cv2
import matplotlib.pyplot as plt
import numpy as np
import io
import os
import urllib, base64
from django.conf import settings
from .forms import ImageUploadForm


def home(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = form.cleaned_data['image']
            # load image and convert to a format compatible with OpenCV
            image = cv2.imdecode(np.fromstring(image_file.read(), np.uint8), cv2.IMREAD_COLOR)
            # convert BGR to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
            # define scale factor
            scale_factor_1 = 3.0  # increase size by 3 times
            scale_factor_2 = 1/3.0  # decrease size by 3 times
            
            # get original image dimensions
            height, width = image_rgb.shape[:2]
            
            # calculate new image dimensions for zoomed image
            new_height = int(height * scale_factor_1)
            new_width = int(width * scale_factor_1)
            zoomed_image = cv2.resize(image_rgb, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
            
            # calculate new image dimensions for scaled image
            new_height1 = int(height * scale_factor_2)
            new_width1 = int(width * scale_factor_2)
            scaled_image = cv2.resize(image_rgb, (new_width1, new_height1), interpolation=cv2.INTER_AREA)
            
            # create subplots
            fig, axs = plt.subplots(1, 3, figsize=(10, 4))
            axs[0].imshow(image_rgb)
            axs[0].set_title(f'Original Image Shape: {image_rgb.shape}')
            axs[1].imshow(zoomed_image)
            axs[1].set_title(f'Zoomed Image Shape: {zoomed_image.shape}')
            axs[2].imshow(scaled_image)
            axs[2].set_title(f'Scaled Image Shape: {scaled_image.shape}')
            
            # remove ticks from the subplots
            for ax in axs:
                ax.set_xticks([])
                ax.set_yticks([])
            
            # display subplots
            plt.tight_layout()

            # save plot to a BytesIO object
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            string = base64.b64encode(buf.read())
            uri = urllib.parse.quote(string)
            
            # ensure the media directory exists
            if not os.path.exists(settings.MEDIA_ROOT):
                os.makedirs(settings.MEDIA_ROOT)

            # save the plot as a file
            download_path = os.path.join(settings.MEDIA_ROOT, 'plot.png')
            plt.savefig(download_path)

            # render HTML template with the image
            return render(request, 'result.html', {'data': uri, 'download_url': settings.MEDIA_URL + 'plot.png'})
    else:
        form = ImageUploadForm()

        return render(request, 'home.html', {'form': form})

