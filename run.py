import argparse
from color_correction import Main
import os

def parse_args():
    parser = argparse.ArgumentParser(description="Color Blindness Correction Tool")
    
    # Input and output file paths
    parser.add_argument('-input', type=str, help='Path to the input image.', required=True)
    parser.add_argument('-output', type=str, help='Directory to save the corrected image.', required=True)
    
    # Type of color blindness and severity
    parser.add_argument('-type', type=str, choices=['protanopia', 'deuteranopia', 'tritanopia', 'protanomaly', 'deuteranomaly', 'tritanomaly'], required=True, help='Color blindness type.')
    parser.add_argument('-severity', type=float, choices=[0.25, 0.5, 0.75], required=True, help='Severity level for the correction (0.25, 0.5, or 0.75).')
    
    # Option to return the corrected image in different formats
    parser.add_argument('-return_type', type=str, choices=['save', 'np', 'pil'], default='save', help='Specify how to return the corrected image (save to file, return as numpy array, or return as PIL image).')

    return parser.parse_args()

def main():
    args = parse_args()
    
    # Ensure the output directory exists
    if not os.path.isdir(args.output):
        print(f"Error: The output directory '{args.output}' does not exist.")
        return
    
    # Correct the image
    Main.correctImage(
        get_path=args.input,
        blindness_type=args.type,
        severity_level=args.severity,
        return_type_image=args.return_type,
        save_path=f"{args.output}/{args.type}_{args.severity}_{args.input.split('/')[-1]}"
    )
    print(f"Image corrected and saved in {args.output}")

if __name__ == '__main__':
    main()
