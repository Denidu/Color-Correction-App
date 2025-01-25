import numpy as np
from PIL import Image

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
    def colour_correction_matrix(blindness_type, severity_level):
        # Define the matrix values based on the type of color blindness
        if blindness_type == 'protanopia':
            matrix = np.array([[1 - severity_level / 2, severity_level / 2, 0],
                               [severity_level / 2, 1 - severity_level / 2, 0],
                               [severity_level / 4, severity_level / 4, 1 - (severity_level * 2) / 4]]).T

        elif blindness_type == 'deuteranopia':
            matrix = np.array([[1 - severity_level / 2, 0, severity_level / 2],
                               [severity_level / 2, 1 - severity_level / 2, 0],
                               [severity_level / 4, severity_level / 4, 1 - (severity_level * 2) / 4]]).T

        elif blindness_type == 'tritanopia':
            matrix = np.array([[1 - severity_level / 2, 0, 0],
                               [0, 1 - severity_level / 2, severity_level / 2],
                               [severity_level / 4, severity_level / 4, 1 - (severity_level * 2) / 4]]).T

        elif blindness_type == 'protanomaly':
            matrix = np.array([[1 - severity_level / 2, severity_level / 2, 0],
                               [severity_level / 2, 1 - severity_level / 2, 0],
                               [severity_level / 4, severity_level / 4, 1 - severity_level / 4]]).T

        elif blindness_type == 'deuteranomaly':
            matrix = np.array([[1 - severity_level / 2, 0, severity_level / 2],
                               [severity_level / 2, 1 - severity_level / 2, 0],
                               [severity_level / 4, severity_level / 4, 1 - severity_level / 4]]).T

        elif blindness_type == 'tritanomaly':
            matrix = np.array([[1 - severity_level / 2, 0, 0],
                               [0, 1 - severity_level / 2, severity_level / 2],
                               [severity_level / 4, severity_level / 4, 1 - severity_level / 4]]).T

        return matrix


class LoadImage:
    
    @staticmethod
    def process_RGB(path):
        image = Image.open(path)
        rgb_image = np.array(image.convert('RGB')) / 255  # Ensure the image is in RGB format
        return rgb_image


    @staticmethod
    def process_LMS(path):
        rgb_image = np.array(Image.open(path)) / 255
        lms_image = np.dot(rgb_image[:, :, :3], Modify.RGB_TO_LMS())
        return lms_image
