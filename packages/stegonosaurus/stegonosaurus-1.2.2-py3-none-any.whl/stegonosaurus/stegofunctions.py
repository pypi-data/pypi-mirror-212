"""This library runs on PIL"""
from PIL import Image
from . import stegoutils as su
from . import stegoexceptions as se


def inspect(img: Image) -> str:
    """Returns each individual pixel and additional information
    on the image input.
    """
    info_string = ""
    valid = "No"
    generator = su.image_reader(img)

    for i in generator:
        info_string += i

    info_string += "\n" + "Filename: "

    if hasattr(img, "filename"):
        info_string += img.filename

    if su.validate_image_format(img):
        valid = "Yes"

    info_string += ("\nFormat: " + img.format + "\nMode: " + img.mode +
                    "\nSize: " + str(img.width) + "x" + str(img.height) +
                    "\nValid: " + valid)

    return info_string


def blacken(img: Image) -> Image:
    """Creates an all-black image with the provided image's
    dimensions.
    """
    new_img = img.copy()

    if su.validate_image_format(img):
        pix_x = img.size[0]
        pix_y = img.size[1]
        width = img.width
        height = img.height

        for pix_x in range(0, width):
            for pix_y in range(0, height):
                new_img.putpixel((pix_x, pix_y), (0, 0, 0, 255))
    else:
        raise se.StegonosaurusIncorrectFormatError("The file must " +
                                                       "be a multi-band " +
                                                       ".png image.")

    return new_img


def decode(img: Image, mode: str) -> Image:
    """Decodes an image with an encoded message."""
    new_img = img.copy()

    if su.validate_decode_mode(mode):
        if su.validate_image_format(img):
            pix_x = 0
            pix_y = 0
            width = img.size[0]
            height = img.size[1]

            # Iterate the image to look for odd pixels.
            for pix_x in range(0, width):
                for pix_y in range(0, height):
                    pix = img.getpixel((pix_x, pix_y))

                    if pix[2] % 2 == 1:
                        # Odd pixels are turned red.
                        new_img.putpixel((pix_x, pix_y), (255, 0, 0, 255))
                    else:
                        # If the mode is "B", even pixels are turned black.
                        if mode.lower() == "b":
                            new_img.putpixel((pix_x, pix_y), (0, 0, 0, 255))

        else:
            raise se.StegonosaurusIncorrectFormatError("The file must be a " +
                                                        "multi-band .png " +
                                                        "image.")
    else:
        raise se.StegonosaurusInvalidDecodeModeError("The provided decode " +
                                                     "mode is invalid.")

    return new_img


def encode(coded: Image, img: Image) -> Image:
    """Encodes the message inside the other image."""
    if (su.validate_image_format(coded) and
        su.validate_image_format(img)):
        if su.validate_images_size(coded, img):
            flat_coded = su.flatten_coded(coded)
            flat_img = su.flatten_image(img)
            pix_x = 0
            pix_y = 0
            width = flat_coded.size[0]
            height = flat_coded.size[1]

            # Copy of the original image.
            new_img = flat_img.copy()

            # Any red pixels on the black image are turned into odd
            # pixels on the original picture.
            for pix_x in range(0, width):
                for pix_y in range(0, height):
                    if flat_coded.getpixel((pix_x, pix_y))[0] > 0:
                        pix = list(flat_img.getpixel((pix_x, pix_y)))
                        pix[2] = pix[2] + 1
                        if len(pix) == 3:
                            pix.append(255)

                        new_img.putpixel((pix_x, pix_y), tuple(pix))

            flat_coded.close()
            flat_img.close()

            return new_img
        else:
            raise se.StegonosaurusIncorrectSizeError("The image with " +
                                                         "the coded " +
                                                         "message should " +
                                                         "be smaller than " +
                                                         "the image where " +
                                                         "the message will " +
                                                         "be hidden.")
    else:
        raise se.StegonosaurusIncorrectFormatError("Both files must be " +
                                                       "multi-band .png " +
                                                       "images.")

    return None
