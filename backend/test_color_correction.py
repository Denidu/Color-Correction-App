import unittest
import os
import cv2
import numpy as np
from PIL import Image
from color_correction import Main
from skimage.metrics import structural_similarity as ssim

class TestColorCorrection(unittest.TestCase):

    def setUp(self):
        """Automatically selects either image or video for testing, prioritizing images."""
        self.uploads_dir = "uploads"
        self.image_files = [f for f in os.listdir(self.uploads_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        self.video_files = [f for f in os.listdir(self.uploads_dir) if f.lower().endswith(('.mp4', '.avi', '.mov'))]

        print(f"Image files found: {self.image_files}")
        print(f"Video files found: {self.video_files}")

        if not self.image_files and not self.video_files:
            raise FileNotFoundError("No image or video files found in the uploads folder.")

        if self.image_files:
            self.test_type = 'image'
            self.test_file = os.path.join(self.uploads_dir, self.image_files[0])
            print(f"Automatically selected Image: {self.test_file}")
        elif self.video_files:
            self.test_type = 'video'
            self.test_file = os.path.join(self.uploads_dir, self.video_files[0])
            print(f"Automatically selected Video: {self.test_file}")

        self.color_blindness_type = "Protanopia"  
        self.severity = "Moderate"

    def tearDown(self):
        """No file deletion needed."""
        pass  

    def calculate_metrics(self, original, corrected):
        """Calculates MSE, PSNR, and SSIM between the original and corrected images."""
        mse = np.mean((original - corrected) ** 2)
        psnr = cv2.PSNR(original, corrected) if mse > 0 else 100
        ssim_score = ssim(original, corrected, multichannel=True, channel_axis=2)
        return mse, psnr, ssim_score

    def extract_frames(self, video_path):
        """Extracts frames from the given video."""
        cap = cv2.VideoCapture(video_path)
        frames = []
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)
        cap.release()
        return frames

    def test_image_color_correction(self):
        """Tests the color correction for an image."""
        if self.test_type != 'image':
            self.skipTest("Skipping image test as no image file is available.")

        corrected_image = Main.processImageCorrection(self.test_file, self.color_blindness_type, self.severity, return_type_image='np')

        original_image = np.array(Image.open(self.test_file))

        mse, psnr, ssim_score = self.calculate_metrics(original_image, corrected_image)

        print(f"Image Correction Accuracy:\nMSE: {mse}\nPSNR: {psnr} dB\nSSIM: {ssim_score}")

        self.assertGreater(psnr, 30)
        self.assertGreater(ssim_score, 0.85)

    def test_video_color_correction(self):
        """Tests the color correction on a video."""
        if self.test_type != 'video':
            self.skipTest("Skipping video test as no video file is available.")

        original_frames = self.extract_frames(self.test_file)
        corrected_frames = []
        temp_save_folder = "processed/temp_video_frames"

        os.makedirs(temp_save_folder, exist_ok=True) 

        for idx, frame in enumerate(original_frames):
            temp_save_path = os.path.join(temp_save_folder, f"frame_{idx}.png")  
            corrected_frame = Main.processImageCorrection(temp_save_path, self.color_blindness_type, self.severity, frame=frame)
            corrected_frames.append(corrected_frame)

        total_mse, total_psnr, total_ssim = 0, 0, 0
        num_frames = len(original_frames)

        for orig, corr in zip(original_frames, corrected_frames):
            mse, psnr, ssim_score = self.calculate_metrics(orig, corr)
            total_mse += mse
            total_psnr += psnr
            total_ssim += ssim_score

        avg_mse = total_mse / num_frames
        avg_psnr = total_psnr / num_frames
        avg_ssim = total_ssim / num_frames

        print(f"Video Correction Accuracy:\nMSE: {avg_mse}\nPSNR: {avg_psnr} dB\nSSIM: {avg_ssim}")

        self.assertGreater(avg_psnr, 30)  
        self.assertGreater(avg_ssim, 0.85) 

if __name__ == '__main__':
    unittest.main()
