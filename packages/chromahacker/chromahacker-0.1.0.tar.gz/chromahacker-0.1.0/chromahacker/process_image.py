import requests
import numpy as np
from PIL import Image
from io import BytesIO

# Send GET request
def url_to_image(url):
    response = requests.get(url)

    # Convert response to image
    image = Image.open(BytesIO(response.content))

    # Convert image to NumPy array
    image_array = np.array(image)

    # Print array shape
    return image_array
