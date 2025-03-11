import customtkinter as ctk
import cv2
import os
from PIL import Image, ImageTk
from tkinter import filedialog
from gui.ctk_config import COLORS, FONTS, PADDING, get_center_position, set_app_icon
from image_processor import white_balance_gray_world, adjust_exposure, reduce_green_tint

class ImageProcessorGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 设置窗口
        self.title("图像处理工具")
        window_width = 1000
        window_height = 320
        self.geometry(get_center_position(window_width, window_height))
        set_app_icon(self)

        # 初始化变量
        self.input_dir = ""
        self.output_dir = ""
        self.current_image = None
        self.preview_image = None

        self.create_widgets()

    def create_widgets(self):
        # 创建主框架
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)

        # 左侧控制面板
        control_frame = ctk.CTkFrame(self)
        control_frame.grid(row=0, column=0, padx=PADDING["medium"], pady=PADDING["medium"], sticky="nsew")

        # 目录选择
        ctk.CTkLabel(control_frame, text="输入目录：", font=FONTS["subtitle"]).pack(pady=(PADDING["medium"], 0))
        self.input_dir_button = ctk.CTkButton(control_frame, text="选择输入目录", command=self.select_input_dir)
        self.input_dir_button.pack(pady=PADDING["small"], padx=PADDING["medium"], fill="x")

        ctk.CTkLabel(control_frame, text="输出目录：", font=FONTS["subtitle"]).pack(pady=(PADDING["medium"], 0))
        self.output_dir_button = ctk.CTkButton(control_frame, text="选择输出目录", command=self.select_output_dir)
        self.output_dir_button.pack(pady=PADDING["small"], padx=PADDING["medium"], fill="x")

        # 处理按钮
        self.process_button = ctk.CTkButton(control_frame, text="开始处理", command=self.process_images,
                                          fg_color=COLORS["success"])
        self.process_button.pack(pady=PADDING["large"], padx=PADDING["medium"], fill="x")

        # 右侧预览区域
        preview_frame = ctk.CTkFrame(self)
        preview_frame.grid(row=0, column=1, padx=PADDING["medium"], pady=PADDING["medium"], sticky="nsew")
        preview_frame.grid_columnconfigure(0, weight=1)
        preview_frame.grid_rowconfigure(0, weight=1)

        self.preview_label = ctk.CTkLabel(preview_frame, text="预览区域")
        self.preview_label.grid(row=0, column=0, sticky="nsew")

    def select_input_dir(self):
        self.input_dir = filedialog.askdirectory(title="选择输入目录")
        if self.input_dir:
            self.input_dir_button.configure(text=f"输入目录: {os.path.basename(self.input_dir)}")
            self.load_preview_image()

    def select_output_dir(self):
        self.output_dir = filedialog.askdirectory(title="选择输出目录")
        if self.output_dir:
            self.output_dir_button.configure(text=f"输出目录: {os.path.basename(self.output_dir)}")

    def load_preview_image(self):
        if not self.input_dir:
            return

        # 获取第一张图片
        for filename in os.listdir(self.input_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                img_path = os.path.join(self.input_dir, filename)
                self.current_image = cv2.imread(img_path)
                if self.current_image is not None:
                    self.update_preview()
                break

    def update_preview(self):
        if self.current_image is None:
            return

        # 处理图像
        preview = self.current_image.copy()
        preview = white_balance_gray_world(preview)
        preview = reduce_green_tint(preview)
        preview = adjust_exposure(preview, target_mean=180)

        # 调整预览图像大小
        h, w = preview.shape[:2]
        max_size = 500
        if h > w:
            new_h = max_size
            new_w = int(w * max_size / h)
        else:
            new_w = max_size
            new_h = int(h * max_size / w)

        preview = cv2.resize(preview, (new_w, new_h))
        preview = cv2.cvtColor(preview, cv2.COLOR_BGR2RGB)

        # 转换为PhotoImage
        image = Image.fromarray(preview)
        photo = ImageTk.PhotoImage(image)

        # 更新预览
        self.preview_label.configure(image=photo, text="")
        self.preview_image = photo

    def process_images(self):
        if not self.input_dir or not self.output_dir:
            self.process_button.configure(text="请选择输入和输出目录", fg_color=COLORS["error"])
            self.after(2000, lambda: self.process_button.configure(text="开始处理", fg_color=COLORS["success"]))
            return

        try:
            os.makedirs(self.output_dir, exist_ok=True)
            processed_count = 0
            error_count = 0
            
            for filename in os.listdir(self.input_dir):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    try:
                        img_path = os.path.join(self.input_dir, filename)
                        img = cv2.imread(img_path)
                        if img is None:
                            raise ValueError(f"无法读取图像文件：{filename}")
                        
                        # 处理图像
                        img = white_balance_gray_world(img)
                        img = reduce_green_tint(img)
                        img = adjust_exposure(img, target_mean=180)
                        
                        # 保存处理后的图像
                        output_path = os.path.join(self.output_dir, filename)
                        if not cv2.imwrite(output_path, img):
                            raise IOError(f"无法保存图像文件：{filename}")
                        
                        processed_count += 1
                    except Exception as e:
                        error_count += 1
                        print(f"处理图像 {filename} 时出错：{str(e)}")

            # 更新处理结果
            if error_count == 0:
                result_text = f"处理完成！成功处理 {processed_count} 张图像"
                button_color = COLORS["success"]
            else:
                result_text = f"处理完成，但有 {error_count} 个错误"
                button_color = COLORS["warning"]

            self.process_button.configure(text=result_text, fg_color=button_color)
            self.after(2000, lambda: self.process_button.configure(text="开始处理", fg_color=COLORS["success"]))

        except Exception as e:
            error_msg = f"处理过程出错：{str(e)}"
            self.process_button.configure(text=error_msg, fg_color=COLORS["error"])
            self.after(2000, lambda: self.process_button.configure(text="开始处理", fg_color=COLORS["success"]))

if __name__ == "__main__":
    app = ImageProcessorGUI()
    app.mainloop()