import pillow


from PIL import Image
from pyzbar.pyzbar import decode

def read_barcode(image_path):
    # Open the image file
    img = Image.open(image_path)w

    # Decode the barcode
    barcodes = decode(img)

    # Check if any barcodes are found
    if not barcodes:
        print("No barcodes found.")
        return None

    # Display the data from each barcode
    for barcode in barcodes:
        print("Barcode Type:", barcode.type)
        print("Barcode Data:", barcode.data.decode("utf-8"))

# Example usage
image_path = 'path_to_your_image.jpg'  # Replace with the path to your image
read_barcode(image_path)