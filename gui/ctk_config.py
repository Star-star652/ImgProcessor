import customtkinter as ctk
import os

# 设置外观模式和默认颜色主题
ctk.set_appearance_mode("System")  # 系统模式，会根据系统设置自动切换明暗主题
ctk.set_default_color_theme("blue")  # 默认颜色主题

# 自定义颜色
COLORS = {
    "primary": "#007acc",  # 主要颜色
    "secondary": "#3c3c3c",  # 次要颜色
    "background": "#1e1e1e",  # 背景颜色
    "text": "#d4d4d4",  # 文本颜色
    "success": "#4caf50",  # 成功颜色
    "warning": "#ff9800",  # 警告颜色
    "error": "#f44336",  # 错误颜色
}

# 字体设置
FONTS = {
    "default": ("Segoe UI", 10),
    "title": ("Segoe UI", 14, "bold"),
    "subtitle": ("Segoe UI", 12),
    "small": ("Segoe UI", 8),
}

# 边距和间距设置
PADDING = {
    "small": 5,
    "medium": 10,
    "large": 20,
}

# 窗口尺寸设置
SIZES = {
    "login": "600x300",
    "register": "300x400",
    "interface": "600x300",
    "apikey": "600x268",
    "runner": "1000x620",
    "nodedr": "600x400"
}

# 获取屏幕中心位置
def get_center_position(width, height):
    """
    计算窗口在屏幕中心的位置
    """
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()  # 不显示临时窗口
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()
    
    x = int((screen_width - width) / 2)
    y = int((screen_height - height) / 2)
    return f"{width}x{height}+{x}+{y}"

# 设置应用图标
def set_app_icon(window):
    """
    设置应用图标
    """
    icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "ndr-icon.ico")
    if os.path.exists(icon_path):
        window.iconbitmap(icon_path)