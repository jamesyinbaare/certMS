import shutil
from io import BytesIO
from pathlib import Path

import typer
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
from PIL import Image

CERT_ID_CROP_BOX = (
    LEFT,
    TOP,
    RIGHT,
    LOWER,
) = (100, 50, 430, 160)

STUDENT_ID_CROP_BOX = (
    LEFT,
    TOP,
    RIGHT,
    LOWER,
) = (1220, 1946, 1532, 2015)


app = typer.Typer()


@app.command()
def version():
    """Intro"""
    print("CLI tool to extract certificates number from certificate")


@app.command()
def extract(path: Path, output_folder: Path):
    cropped_images = crop_images(path, [CERT_ID_CROP_BOX, STUDENT_ID_CROP_BOX])
    results = []
    for images in cropped_images:
        (regions, file_name) = images
        res = []
        for img in regions:
            ocr_result = ocr(img)
            value = ocr_result["pages"][0]["blocks"][0]["lines"][0]["words"][0]["value"]
            res.append(value)
        new_file_name = "_".join(res)
        rename_cert(file_name, output_folder / f"{new_file_name}.jpg")
        results.append((res, file_name))


def rename_cert(src_file, dest_file):
    """
    Make a copy of the scanned certificate and save it
    """
    try:
        shutil.copy2(src_file, dest_file)
        print(f"File '{src_file}' successfully copied to '{dest_file}'.")
    except FileNotFoundError:
        print(f"Error: File '{src_file}' not found.")
    except shutil.SameFileError:
        print(f"Error: Source and destination files are the same.")


def crop_images(input_folder, crop_boxes):
    "Returns a list of crop images and associated crop file"

    # Loop through all files in the input folder
    for file_path in Path(input_folder).glob("*.jpg"):
        img = Image.open(file_path)
        cropped_imgs_with_file_name = []
        cropped_imgs = []
        for crop_box in crop_boxes:
            cropped_img = img.crop(crop_box)
            cropped_imgs.append(cropped_img)

        cropped_imgs_with_file_name.append((cropped_imgs, file_path))
        cropped_imgs = []
        img.close()

    return cropped_imgs_with_file_name


def ocr(image):
    """
    Performs ocr and return the results
    """
    stream = BytesIO()
    image.save(stream, format="JPEG")
    binary_data = stream.getvalue()
    doc = DocumentFile.from_images(binary_data)
    predictor = ocr_predictor(pretrained=True)
    result = predictor(doc)
    json_export = result.export()
    stream.close()
    return json_export


if __name__ == "__main__":
    app()
