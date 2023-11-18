from pathlib import Path

import typer
from PIL import Image

app = typer.Typer()


def crop_images(input_folder, output_folder, crop_boxes):
    "Returns a list of crop images and associated crop file"
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)

    # Loop through all files in the input folder
    for file_path in Path(input_folder).glob("*.jpg"):
        # Open the image file
        img = Image.open(file_path)
        cropped_imgs_with_file_name = []
        cropped_imgs = []
        # output_file_path = output_path / file_path
        for crop_box in crop_boxes:
            cropped_img = img.crop(crop_box)
            cropped_imgs.append(cropped_img)

        cropped_imgs_with_file_name.append((cropped_imgs, file_path))
        cropped_imgs = []
        img.close()

    return cropped_imgs_with_file_name


@app.command()
def version():
    """Intro"""
    print("CLI tool to extract certificates number from certificate")


@app.command()
def extract(path: Path, output_folder: Path):
    pass


if __name__ == "__main__":
    app()
