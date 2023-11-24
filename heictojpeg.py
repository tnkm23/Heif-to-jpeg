from PIL import Image
import pillow_heif
import pathlib
import os
import argparse
import sys

# コマンドライン引数の処理
parser = argparse.ArgumentParser(description="Convert HEIC images to JPEG")
parser.add_argument("dir", nargs="?", help="Directory containing HEIC images to convert")
args = parser.parse_args()
dir = args.dir

# もし引数 dir が指定されていない場合、スクリプトの存在するフォルダを対象にする
if dir is None:
    script_directory = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))
    dir = script_directory

def heic_jpg(image_path, save_path):
    heif_file = pillow_heif.read_heif(image_path)
    for img in heif_file: 
        image = Image.frombytes(
            img.mode,
            img.size,
            img.data,
            'raw',
            img.mode,
            img.stride,
        )
    image.save(save_path, "JPEG")

image_dir = pathlib.Path(dir)

# JPEG保存用のディレクトリが存在しない場合、新規作成する
jpeg_dir = image_dir / "JPEG"
if not jpeg_dir.exists():
    os.makedirs(jpeg_dir)

heic_path = list(image_dir.glob('**/*.heic'))

for i in heic_path:
    image_path = str(i)
    save_path = str(jpeg_dir / i.stem) + '.jpg'
    print(save_path)
    heic_jpg(image_path, save_path)
