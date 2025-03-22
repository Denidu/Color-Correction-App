import numpy as np
from color_correction import Main
import os

def correct_color(input_path, blindness_type, severity, output_image_path=None):
    """
    This function applies color correction based on the user's chosen color blindness type and severity.
    - For images: The corrected image will be saved to output_image_path.
    - For video frames: The corrected frame is returned directly.
    """
    if isinstance(input_path, str):
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input image path '{input_path}' does not exist.")

        if output_image_path:  
            Main.correctImage(
                get_path=input_path,
                blindness_type=blindness_type,
                severity_level=severity,
                return_type_image='save', 
                save_path=output_image_path  
            )
            print(f"Image corrected and saved to {output_image_path}")
        else:
            corrected_image = Main.correctImage(
                get_path=input_path,
                blindness_type=blindness_type,
                severity_level=severity,
                return_type_image='array' 
            )
            return corrected_image

    elif isinstance(input_path, np.ndarray): 
        corrected_frame = Main.correctImage(
            get_path=None,
            blindness_type=blindness_type,
            severity_level=severity,
            return_type_image='array'
        )
        return corrected_frame
    else:
        raise ValueError("Input path must be either a valid file path or a numpy array (for video frames).")
