from io import BytesIO
from pathlib import Path

import typer
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
    """
    The extract command performs ocr on the images in the given path and out a csv
    file containing the extracted information for each image
    """
    cropped_images = crop_images(path, [CERT_ID_CROP_BOX, STUDENT_ID_CROP_BOX])
    with open(output_folder / "results.csv", "w") as orc_res:
        orc_res.write("CERT_ID, STUDENT_ID,FILE_PATH")
        orc_res.write("\n")
        for images in cropped_images:
            (regions, file_name) = images
            res = []
            for img in regions:
                ocr_result = ocr(img)
                value = ocr_result["pages"][0]["blocks"][0]["lines"][0]["words"][0]["value"]
                res.append(value)
            res.append(str(file_name))  # add the file name
            cert_and_student_id = ",".join(res)
            orc_res.write(cert_and_student_id)
            orc_res.write("\n")


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
    from doctr.io import DocumentFile
    from doctr.models import ocr_predictor

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
