import numpy as np
from PIL import Image
import os

class Modify:

    @staticmethod
    def RGB_TO_LMS():
        return np.array([[17.8824, 43.5161, 4.11935],
                         [3.45565, 27.1554, 3.86714],
                         [0.0299566, 0.184309, 1.46709]]).T

    @staticmethod
    def LMS_TO_RGB():
        return np.array([[0.0809, -0.1305, 0.1167],
                         [-0.0102, 0.0540, -0.1136],
                         [-0.0004, -0.0041, 0.6935]]).T

    @staticmethod
    def color_adjustment_matrix(color_vision_deficiency_type, severity_level):
        color_vision_deficiency_type = color_vision_deficiency_type.lower()

        severity_map = {
            'mild': 0.25,
            'moderate': 0.5,
            'severe': 0.75
        }

        if isinstance(severity_level, str):
            severity_level = severity_map.get(severity_level.lower(), 0.5)

        if color_vision_deficiency_type == 'protanopia':
            matrix = np.array([[1 - severity_level / 2, severity_level / 2, 0],
                               [severity_level / 2, 1 - severity_level / 2, 0],
                               [severity_level / 4, severity_level / 4, 1 - (severity_level * 2) / 4]]).T

        elif color_vision_deficiency_type == 'deuteranopia':
            matrix = np.array([[1 - severity_level / 2, 0, severity_level / 2],
                               [severity_level / 2, 1 - severity_level / 2, 0],
                               [severity_level / 4, severity_level / 4, 1 - (severity_level * 2) / 4]]).T

        elif color_vision_deficiency_type == 'tritanopia':
            matrix = np.array([[1 - severity_level / 2, 0, 0],
                               [0, 1 - severity_level / 2, severity_level / 2],
                               [severity_level / 4, severity_level / 4, 1 - (severity_level * 2) / 4]]).T

        elif color_vision_deficiency_type == 'protanomaly':
            matrix = np.array([[1 - severity_level / 2, severity_level / 2, 0],
                               [severity_level / 2, 1 - severity_level / 2, 0],
                               [severity_level / 4, severity_level / 4, 1 - severity_level / 4]]).T

        elif color_vision_deficiency_type == 'deuteranomaly':
            matrix = np.array([[1 - severity_level / 2, 0, severity_level / 2],
                               [severity_level / 2, 1 - severity_level / 2, 0],
                               [severity_level / 4, severity_level / 4, 1 - severity_level / 4]]).T

        elif color_vision_deficiency_type == 'tritanomaly':
            matrix = np.array([[1 - severity_level / 2, 0, 0],
                               [0, 1 - severity_level / 2, severity_level / 2],
                               [severity_level / 4, severity_level / 4, 1 - severity_level / 4]]).T

        else:
            raise ValueError(f"Unknown blindness type: {color_vision_deficiency_type}")

        return matrix


class LoadImage:
    
    @staticmethod
    def convert_image_to_RGB(input_location):
        if input_location is None:
            raise ValueError("The provided image location is None.")

        if not os.path.exists(input_location):
            raise FileNotFoundError(f"Image not found: {input_location}")
        
        try:
            image = Image.open(input_location)
            rgb_image = np.array(image.convert('RGB')) / 255 
            return rgb_image
        except Exception as e:
            raise ValueError(f"Error processing image at {input_location}: {str(e)}")

    @staticmethod
    def convert_image_to_LMS(input_location):
        if input_location is None:
            raise ValueError("The provided image path is None.")

        if not os.path.exists(input_location):
            raise FileNotFoundError(f"Image not found: {input_location}")
        
        try:
            rgb_image = np.array(Image.open(input_location)) / 255
            lms_image = np.dot(rgb_image[:, :, :3], Modify.RGB_TO_LMS())
            return lms_image
        except Exception as e:
            raise ValueError(f"Error processing image at {input_location}: {str(e)}")