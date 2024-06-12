import os
import cv2
import requests
import pandas as pd
from PIL import Image
from io import BytesIO
import numpy as np

API_KEY = '7r0hFwqlOM-3uubvc9-nDlR5quL6x2W6'
API_SECRET = 'asgRrTEi10PLWlWuyMyB3MW42TbiypcU'

# URL for the Face++ API endpoint
url = 'https://api-us.faceplusplus.com/facepp/v3/detect'

def detectFaces(imgPath):

    # Open the image file
    with open(imgPath, 'rb') as f:
        # Prepare the request parameters
        files = {'image_file': f}
        data = {
            'api_key': API_KEY,
            'api_secret': API_SECRET,
            'return_attributes': 'gender'  # Optional: Include other attributes if needed
        }

        # Send the POST request to the Face++ API
        response = requests.post(url, files=files, data=data)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        result = response.json()
        
        # Extract the number of faces detected
        num_faces = len(result['faces'])
        print("Number of persons in the image:", num_faces)
        return num_faces
    else:
        print("Error:", response.text)
        return 0
    

def avgFaces():

    main_folder_path = os.getcwd() + "\\stable_diffusion"
    state = []
    gender = []
    avg = []
    for root, dirs, files in os.walk(main_folder_path):
        
        for subdir in dirs:
            subfolder_path = os.path.join(root, subdir)
            print("Processing images in subfolder:", subfolder_path)

            # getting the details of state and gender
            temp = subdir.split('_')
            if (len(temp) == 3):
                state.append(temp[0] + ' ' + temp[1])
            else:
                state.append(temp[0])
            gender.append(temp[-1])

            # to detect number of faces in image
            cnt = 0
            for filename in os.listdir(subfolder_path):
                if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                    image_path = os.path.join(subfolder_path, filename)
                    cnt += detectFaces(image_path)
            avg.append(cnt/5)
    data = {'State': state, 'Gender': gender, 'Average Number of Persons Detected': avg}
    df = pd.DataFrame(data)

    excel_file_path = 'numFaces.xlsx'
    df.to_excel(excel_file_path, index=False)

avgFaces()
