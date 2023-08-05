# stegonosaurus

*Ver 1.2.2*

Steganography functions packed in a convenient wheel. This library helps encode and decode messages into and out of multi-band .png images. Works with the [Image](https://pillow.readthedocs.io/en/stable/reference/Image.html) module of the Pillow library.

## Requirements
- Python3

## Installing

A simple pip install will do:

`pip install stegonosaurus`

## Functions

### inspect:

Returns a string that contains the values of each pixel in the image along with other relevant info such as image size, format, file name, mode, and whether it can be used with the other functions in the library or not.

### black:

Return an all black copy of a provided image. This helps create a template for images with coded messages used for encoding.

### encode:

Takes two images, a black image with a message in contrasting colors, and the image where the message will be encoded. The image where the message is going to be hidden in is first "flattened" (all pixels with an odd value on their blue component are changed so their blue component's value is even). Afterwards, the image that contains the message is processed, so the same pixels that contain the bright red letters are changed in the other image to pixels where the blue value is odd (harder to express in theory than practice). The image with the bright message has to be smaller or equal in size to the image where the message is going to be hidden in on either axis.

### decode:

Decodes an image with a hidden message. This functions looks for pixels where the blue value is odd, and paints those pixels bright red. This function operates on two modes:

-B,b (for "black"): pixels with an even blue value are colored black, displaying the message in red letters on a black background.
-T,t (for "transparent"): pixels with an odd blue value are colored red, the other pixels remain the same so the message can be displayed on top of the original image.

### Exceptions:

- StegonosaurusIncorrectFormatError: 

  Raised when a function receives a file that isn't a .PNG multiband image.
- StegonosaurusIncorrectSizeError: 

  Raised when the image with the coded message is larger than the image where the message will be hidden.
- StegonosaurusInvalidDecodeModeError (Ver. 1.1.3): 

  Raised when an invalid decode mode is provided.
