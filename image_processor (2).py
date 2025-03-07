import cv2
import numpy as np
import os
from gui.image_processor_gui import ImageProcessorGUI

def white_balance_gray_world(img):
    img = img.astype(np.float32)
    
    avg_b = np.mean(img[:, :, 0])
    avg_g = np.mean(img[:, :, 1])
    avg_r = np.mean(img[:, :, 2])
    
    avg_gray = (avg_b * 0.3 + avg_g * 0.4 + avg_r * 0.3)

    eps = 1e-6
    scale_b = avg_gray / (avg_b + eps)
    scale_g = avg_gray / (avg_g + eps)
    scale_r = avg_gray / (avg_r + eps)
    
    img[:, :, 0] = np.clip(img[:, :, 0] * scale_b, 0, 255)
    img[:, :, 1] = np.clip(img[:, :, 1] * scale_g, 0, 255)
    img[:, :, 2] = np.clip(img[:, :, 2] * scale_r, 0, 255)
    
    return img.astype(np.uint8)

def adjust_exposure(img, target_mean):

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    
    current_mean = np.mean(v)
    if current_mean == 0:
        return img
    
    alpha = target_mean / current_mean
    v_adjusted = cv2.convertScaleAbs(v, alpha=alpha, beta=0)
    
    hsv_adjusted = cv2.merge([h, s, v_adjusted])
    return cv2.cvtColor(hsv_adjusted, cv2.COLOR_HSV2BGR)

def reduce_green_tint(img):
    img = img.astype(np.float32)
    img[:, :, 1] *= 0.7 
    return np.clip(img, 0, 255).astype(np.uint8)

def process_images(input_dir, output_dir):
    """主处理流程"""
    os.makedirs(output_dir, exist_ok=True)
    
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(input_dir, filename)
            img = cv2.imread(img_path)
            if img is None:
                continue
            
            balanced = white_balance_gray_world(img)
            degreened = reduce_green_tint(balanced)
            adjusted = adjust_exposure(degreened, target_mean=180)
            
            output_path = os.path.join(output_dir, filename)
            cv2.imwrite(output_path, adjusted)
            print(f"Processed {filename}")

if __name__ == "__main__":
    # 启动图形界面
    app = ImageProcessorGUI()
    app.mainloop()
    input_dir = "C:/Users/Star/Desktop/Files/2025Spring/BioExperinment/.img/2/2i1"
    output_dir = "C:/Users/Star/Desktop/Files/2025Spring/BioExperinment/.img/2/2o1"
    process_images(input_dir, output_dir)