import cv2
import numpy as np
import os
from PIL import Image
from pathlib import Path

def reduce_green_tint(img):
    img = img.astype(np.float32)
    img[:, :, 1] *= 0.7
    return np.clip(img, 0, 255).astype(np.uint8)

def auto_white_balance(img):
    # 自动白平衡处理
    result = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    avg_a = np.average(result[:, :, 1])
    avg_b = np.average(result[:, :, 2])
    # 降低绿色通道的影响，调整a通道的补偿系数
    result[:, :, 1] = result[:, :, 1] - ((avg_a - 128) * (result[:, :, 0] / 255.0) * 0.2)  # 降低a通道的补偿系数
    result[:, :, 2] = result[:, :, 2] - ((avg_b - 128) * (result[:, :, 0] / 255.0) * 1)
    result = cv2.cvtColor(result, cv2.COLOR_LAB2BGR)
    return result

def adjust_exposure(img):
    # 直方图均衡化处理
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    l = clahe.apply(l)
    lab = cv2.merge((l,a,b))
    adjusted = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    return adjusted

def adjust_contrast(img):
    # 在LAB空间调整对比度
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    # 降低L通道的对比度
    l_mean = np.mean(l)
    l = np.clip((0.8 * (l - l_mean) + l_mean), 0, 255).astype(np.uint8)
    lab = cv2.merge((l, a, b))
    return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

def adjust_saturation(img):
    # 在HSV空间调整饱和度
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    # 提高饱和度
    s = np.clip((s * 2.0), 0, 255).astype(np.uint8)
    hsv = cv2.merge((h, s, v))
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

def process_image(input_path, output_path):
    # 读取图像
    img = cv2.imread(str(input_path))
    if img is None:
        print(f"无法读取图像: {input_path}")
        return False
    
    # 应用自动白平衡
    balanced = auto_white_balance(img)
    balanced = reduce_green_tint(balanced)
    
    # 调整曝光
    exposed = adjust_exposure(balanced)
    
    # 调整对比度
    contrasted = adjust_contrast(exposed)
    
    # 调整饱和度
    processed = adjust_saturation(contrasted)
    
    # 保存处理后的图像
    cv2.imwrite(str(output_path), processed)
    return True

def batch_process_images(input_folder, output_folder):
    # 创建输出文件夹
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 支持的图像格式
    image_extensions = ('.jpg', '.jpeg', '.png', '.bmp')
    
    # 获取输入文件夹中的所有图像
    input_path = Path(input_folder)
    processed_count = 0
    failed_count = 0
    
    for file in input_path.glob('*'):
        if file.suffix.lower() in image_extensions:
            output_file = output_path / f'processed_{file.name}'
            if process_image(file, output_file):
                processed_count += 1
                print(f"成功处理: {file.name}")
            else:
                failed_count += 1
                print(f"处理失败: {file.name}")
    
    print(f"\n处理完成！")
    print(f"成功处理: {processed_count} 张图像")
    print(f"处理失败: {failed_count} 张图像")

if __name__ == "__main__":
    # 设置输入和输出文件夹
    input_folder = input("请输入源图像文件夹路径: ")
    output_folder = input("请输入处理后图像保存文件夹路径: ")
    
    # 执行批量处理
    batch_process_images(input_folder, output_folder)