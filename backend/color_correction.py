import argparse
import os
import numpy as np
from PIL import Image
import cv2
from utils import Modify, LoadImage

class Main:
    @staticmethod
    def processImageCorrection(get_path: str,
                     blindness_type: str,
                     severity_level: float,
                     return_type_image: str = 'save',
                     save_path: str = None,
                     frame: np.ndarray = None):

        if frame is not None:
            rgb_image = frame
        else:
            rgb_image = LoadImage.convert_image_to_RGB(get_path)

        matrix = Modify.color_adjustment_matrix(blindness_type, severity_level)
        corrected_image = np.uint8(np.dot(rgb_image, matrix) * 255)

        if return_type_image == 'save':
            assert save_path is not None, 'Save path is not given for image!'
            cv2.imwrite(save_path, corrected_image)
            return
        
        if return_type_image == 'np':
            return corrected_image
        
        if return_type_image == 'pil':
            return Image.fromarray(corrected_image)

def parse_args():
    parse = argparse.ArgumentParser(description='Color Correct Images for Color-Blindness')

    parse.add_argument('-input', type=str, help='Location to input an image.')
    parse.add_argument('-output', type=str, help='Location to save the output image dir.')

    parse.add_argument('-type', type=str, choices=['protanopia', 'deuteranopia', 'tritanopia', 'protanomaly', 'deuteranomaly', 'tritanomaly'], required=True, help='Type of color blindness.')
    parse.add_argument('-severity', type=float, choices=[0.25, 0.5, 0.75], required=True, help='Severity level of the color blindness.')

    parse.add_argument('-return_type', type=str, choices=['save', 'np', 'pil'], default='save', help='Return type of the corrected image.')
    
    args = parse.parse_args()
    return args


def main():
    args = parse_args()
    get_path = args.input
    name_of_image = get_path.split('/')[-1]
    image_output_path = args.output

    assert os.path.isdir(image_output_path), 'Output location should be a Directory.'

    Main.processImageCorrection(get_path=get_path,
                      blindness_type=args.type,
                      severity_level=args.severity,
                      return_type_image=args.return_type,
                      save_path='{}/{}_{}_{}.{}'.format(image_output_path, args.type, args.severity, name_of_image, 'png'))

    print('ReColorLib Completed running! Check output Image in {}'.format(image_output_path))


if __name__ == '__main__':
    main()




    
