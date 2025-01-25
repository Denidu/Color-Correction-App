import argparse
import os
import numpy as np
from PIL import Image
import cv2
from utils import Modify, LoadImage

class Main:

    @staticmethod
    def correctImage(get_path: str,
                     blindness_type: str,
                     severity_level: float,
                     return_type_image: str = 'save',
                     save_path: str = None):
        
        # Load image in RGB
        rgb_image = LoadImage.process_RGB(get_path)

        # Get the color blindness matrix based on the user's choice
        matrix = Modify.colour_correction_matrix(blindness_type, severity_level)
        
        # Apply the matrix to the image
        corrected_image = np.uint8(np.dot(rgb_image, matrix) * 255)

        # Return or save the image
        if return_type_image == 'save':
            assert save_path is not None, 'Save path is not provided for image!'
            cv2.imwrite(save_path, corrected_image)
            return
        
        if return_type_image == 'np':
            return corrected_image
        
        if return_type_image == 'pil':
            return Image.fromarray(corrected_image)


def parse_args():
    parse = argparse.ArgumentParser(description='Colour Correct Images for Colour-Blindness')
    
    # Input and output file paths
    parse.add_argument('-input', type=str, help='Path to input image.')
    parse.add_argument('-output', type=str, help='Path to save the output image dir.')
    
    # Type and severity of color blindness
    parse.add_argument('-type', type=str, choices=['protanopia', 'deuteranopia', 'tritanopia', 'protanomaly', 'deuteranomaly', 'tritanomaly'], required=True, help='Type of color blindness.')
    parse.add_argument('-severity', type=float, choices=[0.25, 0.5, 0.75], required=True, help='Severity level of the color blindness.')
    
    # Options for how to return the corrected image
    parse.add_argument('-return_type', type=str, choices=['save', 'np', 'pil'], default='save', help='Return type of the corrected image.')
    
    args = parse.parse_args()
    return args


def main():
    args = parse_args()
    get_path = args.input
    name_of_image = get_path.split('/')[-1]
    image_output_path = args.output
    
    # Ensure the output directory exists
    assert os.path.isdir(image_output_path), 'Output path should be a Directory.'

    # Correct the image based on user input
    Main.correctImage(get_path=get_path,
                      blindness_type=args.type,
                      severity_level=args.severity,
                      return_type_image=args.return_type,
                      save_path='{}/{}_{}_{}.{}'.format(image_output_path, args.type, args.severity, name_of_image, 'png'))

    print('ReColorLib Completed running! Check output Image in {}'.format(image_output_path))


if __name__ == '__main__':
    main()
