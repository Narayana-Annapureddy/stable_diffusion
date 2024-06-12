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


def boundingBox(img, subdir):

    with open(img, 'rb') as f:
        files = {'image_file': f}
        params = {
            'api_key': API_KEY,
            'api_secret': API_SECRET,
            'return_attributes': 'gender,age,smiling,emotion',  # Additional attributes to return
        }
        response = requests.post(url, params=params, files=files)
        data = response.json()
        # Extract bounding box coordinates of detected faces
        faces = data['faces']
        for id, face in enumerate(faces):
            face_rectangle = face['face_rectangle']
            left = face_rectangle['left']
            top = face_rectangle['top']
            width = face_rectangle['width']
            height = face_rectangle['height']
            bounding_box = (left, top, width, height)
            
            # To get the cropped image
            # Display the original image and the ROI
            cropImage(img, bounding_box, subdir, img.split('\\')[-1], id)

def cropImage(img, bounding_box, subdir, image_name, id):

    folder_name = os.getcwd() + '\\cropped_images\\' + subdir
    # create a folder if not exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    image_name = image_name[:-5] + '_' + str(id) + '.jpeg'
    image = cv2.imread(img)

    # Bounding box coordinates
    top_left_x = bounding_box[0]
    top_left_y = bounding_box[1]
    width = bounding_box[2]
    height = bounding_box[3]

    # Extract the ROI (Region of Interest)
    roi = image[top_left_y:top_left_y+height, top_left_x:top_left_x+width]
    if roi is None:
        return
    destination_path = os.path.join(folder_name, image_name)
    print(destination_path)
    # Save the ROI as a new image file (optional)
    try:
        cv2.imwrite(destination_path, roi)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    except:
        pass

def avgHexValue(img):

    image = cv2.imread(img)
    if image is None:
       raise ValueError(f"Could not read image: {img}")

    image = image.astype(np.float32)
    average_color = cv2.mean(image)
    bgr_color = tuple(int(round(val)) for val in average_color)
    rgb_color = (int(bgr_color[2]), int(bgr_color[1]), int(bgr_color[0]))
    
    hex_color = '#{:02x}{:02x}{:02x}'.format(rgb_color[0], rgb_color[1], rgb_color[2])
    return hex_color


def get_skin_tone():

    # to get bounding boxes
    main_folder_path = os.getcwd() + "\\stable_diffusion"
    for root, dirs, files in os.walk(main_folder_path):
        for subdir in dirs:
            subfolder_path = os.path.join(root, subdir)
            for filename in os.listdir(subfolder_path):
                if filename.lower().endswith(('jpg', 'jpeg')):
                    image_path = os.path.join(subfolder_path, filename)
                    boundingBox(image_path, subdir)

    main_folder_path = os.getcwd() + "\\cropped_images"
    avg_hex_values = []
    state = []
    gender = []
    file_names = []
    for root, dirs, files in os.walk(main_folder_path):
        for subdir in dirs:
            subfolder_path = os.path.join(root, subdir)

            temp = subdir.split('_')
            for filename in os.listdir(subfolder_path):
                if filename.lower().endswith(('.jpg', '.jpeg', '.png')):

                    if (len(temp) == 3):
                        state.append(temp[0] + ' ' + temp[1])
                    else:
                        state.append(temp[0])
                    gender.append(temp[-1])
                    file_names.append(filename)
                    image_path = os.path.join(subfolder_path, filename)
                    avg_hex_values.append(avgHexValue(image_path))
    
    data = {'State': state, 'Gender': gender, 'FileName': file_names, 'Avg Hex' : avg_hex_values}
    df = pd.DataFrame(data)

    excel_file_path = 'Hex_values.xlsx'
    df.to_excel(excel_file_path, index=False)

get_skin_tone()
