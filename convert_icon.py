from PIL import Image
import os

png_path = "plug.png"
ico_path = "plug.ico"

try:
    img = Image.open(png_path)
    img.save(ico_path, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
    print(f"Successfully converted {png_path} to {ico_path}")
except Exception as e:
    print(f"Error: {e}")
    print("Installing Pillow...")
    import subprocess
    subprocess.run(["python", "-m", "pip", "install", "Pillow"])
    print("Please run this script again after Pillow is installed.")
