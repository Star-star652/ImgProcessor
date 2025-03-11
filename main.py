from gui.image_processor_gui import ImageProcessorGUI
from image_processor import process_images



if __name__ == "__main__":
    # 启动图形界面
    app = ImageProcessorGUI()
    app.mainloop()
    input_dir = "C:/Users/Star/Desktop/Files/2025Spring/BioExperinment/.img/2/2i1"
    output_dir = "C:/Users/Star/Desktop/Files/2025Spring/BioExperinment/.img/2/2o1"
    process_images(input_dir, output_dir)