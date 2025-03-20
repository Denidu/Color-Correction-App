from color_correction import Main
import os

def correct_color(input_image_path, blindness_type, severity, output_image_path):
    """
    This function applies color correction based on the user's chosen color blindness type and severity.
    """
    if not os.path.exists(input_image_path):
        raise FileNotFoundError(f"Input image '{input_image_path}' does not exist.")
    
    # Call the Main.correctImage method from color_correction.py
    Main.correctImage(
        get_path=input_image_path,
        blindness_type=blindness_type,
        severity_level=severity,
        return_type_image='save',  # We want to save the corrected image
        save_path=output_image_path  # Specify where to save the corrected image
    )
    print(f"Image corrected and saved to {output_image_path}")
