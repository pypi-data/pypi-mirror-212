"""Test the functions in the Stegonosaurus library."""
import pytest
from stegonosaurus import stegofunctions as sf
from stegonosaurus import stegoutils as su
from stegonosaurus import stegoexceptions as se


# Image inspection tests:
def test_inspect_valid(raw_image_rgb_png):
    """Test inspection of a valid RGB .png image."""
    assert sf.inspect(raw_image_rgb_png) == ("(0, 255, 255)(0, 255, 255)" +
                                             "(0, 255, 255)(0, 255, 255)\n" +
                                             "Filename: \nFormat: PNG" +
                                             "\nMode: RGB\nSize: 2x2" +
                                             "\nValid: Yes")


def test_inspect_invalid_format(raw_image_rgb_jpeg):
    """Test inspection of an invalid RGB .jpeg image."""
    assert sf.inspect(raw_image_rgb_jpeg) == ("(0, 255, 255)(0, 255, 255)" +
                                             "(0, 255, 255)(0, 255, 255)\n" +
                                             "Filename: \nFormat: JPG" +
                                             "\nMode: RGB\nSize: 2x2" +
                                             "\nValid: No")


def test_inspect_invalid_mode(raw_image_l_png):
    """Test inspection of an invalid single band .png image."""
    assert sf.inspect(raw_image_l_png) == ("0000\n" +
                                            "Filename: \nFormat: PNG" +
                                            "\nMode: L\nSize: 2x2\nValid: No")


# Image blackenning tests:
def test_black_rgb_valid(raw_image_rgb_png):
    """Tests blackenning of a valid RGB .png image."""
    new_image = sf.blacken(raw_image_rgb_png)
    data = []

    for i in su.image_reader(new_image):
        data.append(i)

    assert data == ["(0, 0, 0)", "(0, 0, 0)", "(0, 0, 0)", "(0, 0, 0)"]


def test_black_rgba_valid(raw_image_rgba_png):
    """Tests blackenning of a valid RGBA .png image."""
    new_image = sf.blacken(raw_image_rgba_png)
    data = []

    for i in su.image_reader(new_image):
        data.append(i)

    assert data == ["(0, 0, 0, 255)", "(0, 0, 0, 255)",
                    "(0, 0, 0, 255)", "(0, 0, 0, 255)"]


def test_black_invalid_rgb_jpeg(raw_image_rgb_jpeg):
    """Tests blackenning of an invalid RGB .jpeg image."""
    with pytest.raises(se.StegonosaurusIncorrectFormatError):
        sf.blacken(raw_image_rgb_jpeg)


def test_black_invalid_l_png(raw_image_l_png):
    """Tests blackenning of an invalid single band .png image."""
    with pytest.raises(se.StegonosaurusIncorrectFormatError):
        sf.blacken(raw_image_l_png)


# Image decoding tests:
def test_decode_valid_rgb_png_t(raw_coded_rgb_bright_red_png, raw_image_rgb_png):
    """Tests decoding on a valid RGB .png image, with lower case
    transparent mode.
    """
    encoded = sf.encode(raw_coded_rgb_bright_red_png, raw_image_rgb_png)
    encoded.format = "PNG"
    encoded.mode = "RGB"
    new_image = sf.decode(encoded, "t")
    data = []

    for i in su.image_reader(new_image):
        data.append(i)

    assert data == ["(255, 0, 0)", "(0, 255, 254)",
                    "(0, 255, 254)", "(0, 255, 254)"]


def test_decode_valid_rgba_png_t(raw_coded_rgba_bright_red_png, raw_image_rgba_png):
    """Tests decoding on a valid RGBA .png image, with lower case
    transparent mode.
    """
    encoded = sf.encode(raw_coded_rgba_bright_red_png, raw_image_rgba_png)
    encoded.format = "PNG"
    encoded.mode = "RGBA"
    new_image = sf.decode(encoded, "t")
    data = []

    for i in su.image_reader(new_image):
        data.append(i)

    assert data == ["(255, 0, 0, 255)", "(0, 255, 254, 255)",
                    "(0, 255, 254, 255)", "(0, 255, 254, 255)"]


def test_decode_valid_rgb_png_ut(raw_coded_rgb_bright_red_png, raw_image_rgb_png):
    """Tests decoding on a valid RGB .png image, with upper case
    transparent mode.
    """
    encoded = sf.encode(raw_coded_rgb_bright_red_png, raw_image_rgb_png)
    encoded.format = "PNG"
    encoded.mode = "RGB"
    new_image = sf.decode(encoded, "T")
    data = []

    for i in su.image_reader(new_image):
        data.append(i)

    assert data == ["(255, 0, 0)", "(0, 255, 254)",
                    "(0, 255, 254)", "(0, 255, 254)"]


def test_decode_valid_rgba_png_ut(raw_coded_rgba_bright_red_png, raw_image_rgba_png):
    """Tests decoding on a valid RGBA .png image, with upper case
    transparent mode.
    """
    encoded = sf.encode(raw_coded_rgba_bright_red_png, raw_image_rgba_png)
    encoded.format = "PNG"
    encoded.mode = "RGBA"
    new_image = sf.decode(encoded, "T")
    data = []

    for i in su.image_reader(new_image):
        data.append(i)

    assert data == ["(255, 0, 0, 255)", "(0, 255, 254, 255)",
                    "(0, 255, 254, 255)", "(0, 255, 254, 255)"]


def test_decode_valid_rgb_png_b(raw_coded_rgb_bright_red_png, raw_image_rgb_png):
    """Tests decoding on a valid RGB .png image, with lower case black
    mode.
    """
    encoded = sf.encode(raw_coded_rgb_bright_red_png, raw_image_rgb_png)
    encoded.format = "PNG"
    encoded.mode = "RGB"
    new_image = sf.decode(encoded, "b")
    data = []

    for i in su.image_reader(new_image):
        data.append(i)

    assert data == ["(255, 0, 0)", "(0, 0, 0)", "(0, 0, 0)", "(0, 0, 0)"]


def test_decode_valid_rgba_png_b(raw_coded_rgba_bright_red_png, raw_image_rgba_png):
    """Tests decoding on a valid RGBA .png image, with lower case
    black mode.
    """
    encoded = sf.encode(raw_coded_rgba_bright_red_png, raw_image_rgba_png)
    encoded.format = "PNG"
    encoded.mode = "RGBA"
    new_image = sf.decode(encoded, "b")
    data = []

    for i in su.image_reader(new_image):
        data.append(i)

    assert data == ["(255, 0, 0, 255)", "(0, 0, 0, 255)",
                    "(0, 0, 0, 255)", "(0, 0, 0, 255)"]


def test_decode_valid_rgb_png_ub(raw_coded_rgb_bright_red_png, raw_image_rgb_png):
    """Tests decoding on a valid RGB .png image, with upper case black
    mode.
    """
    encoded = sf.encode(raw_coded_rgb_bright_red_png, raw_image_rgb_png)
    encoded.format = "PNG"
    encoded.mode = "RGB"
    new_image = sf.decode(encoded, "B")
    data = []

    for i in su.image_reader(new_image):
        data.append(i)

    assert data == ["(255, 0, 0)", "(0, 0, 0)", "(0, 0, 0)", "(0, 0, 0)"]


def test_decode_valid_rgba_png_ub(raw_coded_rgba_bright_red_png, raw_image_rgba_png):
    """Tests decoding on a valid RGBA .png image, with upper case black
    mode.
    """
    encoded = sf.encode(raw_coded_rgba_bright_red_png, raw_image_rgba_png)
    encoded.format = "PNG"
    encoded.mode = "RGBA"
    new_image = sf.decode(encoded, "B")
    data = []

    for i in su.image_reader(new_image):
        data.append(i)

    assert data == ["(255, 0, 0, 255)", "(0, 0, 0, 255)",
                    "(0, 0, 0, 255)", "(0, 0, 0, 255)"]


def test_decode_invalid_rgb_jpeg(raw_image_rgb_jpeg):
    """Tests decoding an invalid RGB .jpeg image."""
    with pytest.raises(se.StegonosaurusIncorrectFormatError):
        sf.decode(raw_image_rgb_jpeg, "t")


def test_decode_invalid_l_png(raw_image_l_png):
    """Tests decoding an invalid single band .png image."""
    with pytest.raises(se.StegonosaurusIncorrectFormatError):
        sf.decode(raw_image_l_png, "t")


def test_decode_valid_rgb_png_invalid_string_mode(raw_coded_rgb_bright_red_png, raw_image_rgb_png):
    """Tests decoding on a valid RGB .png image, with an invalid 
    decode mode.
    """
    encoded = sf.encode(raw_coded_rgb_bright_red_png, raw_image_rgb_png)
    encoded.format = "PNG"
    encoded.mode = "RGB"

    with pytest.raises(se.StegonosaurusInvalidDecodeModeError):
        sf.decode(encoded, "CAKE")


def test_decode_valid_rgb_png_invalid_nonstring_mode(raw_coded_rgb_bright_red_png,
                                                    raw_image_rgb_png):
    """Tests decoding on a valid RGB .png image, with an invalid
    non string decode mode.
    """
    encoded = sf.encode(raw_coded_rgb_bright_red_png, raw_image_rgb_png)
    encoded.format = "PNG"
    encoded.mode = "RGB"

    with pytest.raises(se.StegonosaurusInvalidDecodeModeError):
        sf.decode(encoded, 347)


# Image encoding tests:
def test_encode_bright_red_rgb_png(raw_coded_rgb_bright_red_png, raw_image_rgb_png):
    """Tests encoding both valid RGB .png images, with a valid 
    message in bright red.
    """
    new_image = sf.encode(raw_coded_rgb_bright_red_png, raw_image_rgb_png)
    data = []

    for i in su.image_reader(new_image):
        data.append(i)

    assert data == ["(0, 255, 255)", "(0, 255, 254)",
                    "(0, 255, 254)", "(0, 255, 254)"]


def test_encode_bright_red_rgba_png(raw_coded_rgba_bright_red_png, raw_image_rgba_png):
    """Tests encoding both valid RGBA .png images, with a valid 
    message in bright red.
    """
    new_image = sf.encode(raw_coded_rgba_bright_red_png, raw_image_rgba_png)
    data = []

    for i in su.image_reader(new_image):
        data.append(i)

    assert data == ["(0, 255, 255, 255)", "(0, 255, 254, 255)",
                    "(0, 255, 254, 255)", "(0, 255, 254, 255)"]


def test_encode_definitely_red_rgb_png(raw_coded_rgb_definitely_red_png, raw_image_rgb_png):
    """Tests encoding both valid RGB .png images, with a valid 
    message in a color that is clearly red.
    """
    new_image = sf.encode(raw_coded_rgb_definitely_red_png, raw_image_rgb_png)
    data = []

    for i in su.image_reader(new_image):
        data.append(i)

    assert data == ["(0, 255, 255)", "(0, 255, 254)",
                    "(0, 255, 254)", "(0, 255, 254)"]


def test_encode_definitely_red_rgba_png(raw_coded_rgba_definitely_red_png, raw_image_rgba_png):
    """Tests encoding both valid RGBA .png images, with a valid 
    message in a color that is clearly red.
    """
    new_image = sf.encode(raw_coded_rgba_definitely_red_png, raw_image_rgba_png)
    data = []

    for i in su.image_reader(new_image):
        data.append(i)

    assert data == ["(0, 255, 255, 255)", "(0, 255, 254, 255)",
                    "(0, 255, 254, 255)", "(0, 255, 254, 255)"]


def test_encode_barely_red_rgb_png(raw_coded_rgb_barely_red_png, raw_image_rgb_png):
    """Tests encoding both valid RGB .png images, with a valid 
    message in a color that is barely red.
    """
    new_image = sf.encode(raw_coded_rgb_barely_red_png, raw_image_rgb_png)
    data = []

    for i in su.image_reader(new_image):
        data.append(i)

    assert data == ["(0, 255, 255)", "(0, 255, 254)",
                    "(0, 255, 254)", "(0, 255, 254)"]


def test_encode_barely_red_rgba_png(raw_coded_rgba_barely_red_png, raw_image_rgba_png):
    """Tests encoding both valid RGBA .png images, with a valid 
    message in a color that is barely red.
    """
    new_image = sf.encode(raw_coded_rgba_barely_red_png, raw_image_rgba_png)
    data = []

    for i in su.image_reader(new_image):
        data.append(i)

    assert data == ["(0, 255, 255, 255)", "(0, 255, 254, 255)",
                    "(0, 255, 254, 255)", "(0, 255, 254, 255)"]


def test_encode_not_really_red_rgb_png(raw_coded_rgb_not_really_red_png, raw_image_rgb_png):
    """Tests encoding both valid RGB .png images, with a valid 
    message in an invalid shade of red.
    """
    new_image = sf.encode(raw_coded_rgb_not_really_red_png, raw_image_rgb_png)
    data = []

    for i in su.image_reader(new_image):
        data.append(i)

    assert data == ["(0, 255, 254)", "(0, 255, 254)",
                    "(0, 255, 254)", "(0, 255, 254)"]


def test_encode_not_realy_red_rgba_png(raw_coded_rgba_not_really_red_png, raw_image_rgba_png):
    """Tests encoding both valid RGBA .png images, with a valid 
    message in an invalid shade of red.
    """
    new_image = sf.encode(raw_coded_rgba_not_really_red_png, raw_image_rgba_png)
    data = []

    for i in su.image_reader(new_image):
        data.append(i)

    assert data == ["(0, 255, 254, 255)", "(0, 255, 254, 255)",
                    "(0, 255, 254, 255)", "(0, 255, 254, 255)"]


def test_encode_bright_green_rgb_png(raw_coded_rgb_bright_green_png, raw_image_rgb_png):
    """Tests encoding both valid RGB .png images, with a valid 
    message in bright green.
    """
    new_image = sf.encode(raw_coded_rgb_bright_green_png, raw_image_rgb_png)
    data = []

    for i in su.image_reader(new_image):
        data.append(i)

    assert data == ["(0, 255, 255)", "(0, 255, 254)",
                    "(0, 255, 254)", "(0, 255, 254)"]


def test_encode_bright_green_rgba_png(raw_coded_rgba_bright_green_png, raw_image_rgba_png):
    """Tests encoding both valid RGBA .png images, with a valid 
    message in bright green.
    """
    new_image = sf.encode(raw_coded_rgba_bright_green_png, raw_image_rgba_png)
    data = []

    for i in su.image_reader(new_image):
        data.append(i)

    assert data == ["(0, 255, 255, 255)", "(0, 255, 254, 255)",
                    "(0, 255, 254, 255)", "(0, 255, 254, 255)"]


def test_encode_definitely_green_rgb_png(raw_coded_rgb_definitely_green_png, raw_image_rgb_png):
    """Tests encoding both valid RGB .png images, with a valid 
    message in a color that is clearly green.
    """
    new_image = sf.encode(raw_coded_rgb_definitely_green_png, raw_image_rgb_png)
    data = []

    for i in su.image_reader(new_image):
        data.append(i)

    assert data == ["(0, 255, 255)", "(0, 255, 254)",
                    "(0, 255, 254)", "(0, 255, 254)"]


def test_encode_definitely_green_rgba_png(raw_coded_rgba_definitely_green_png, raw_image_rgba_png):
    """Tests encoding both valid RGBA .png images, with a valid 
    message in a color that is clearly green.
    """
    new_image = sf.encode(raw_coded_rgba_definitely_green_png, raw_image_rgba_png)
    data = []

    for i in su.image_reader(new_image):
        data.append(i)

    assert data == ["(0, 255, 255, 255)", "(0, 255, 254, 255)",
                    "(0, 255, 254, 255)", "(0, 255, 254, 255)"]


def test_encode_barely_green_rgb_png(raw_coded_rgb_barely_green_png, raw_image_rgb_png):
    """Tests encoding both valid RGB .png images, with a valid 
    message in a color that is barely green.
    """
    new_image = sf.encode(raw_coded_rgb_barely_green_png, raw_image_rgb_png)
    data = []

    for i in su.image_reader(new_image):
        data.append(i)

    assert data == ["(0, 255, 255)", "(0, 255, 254)",
                    "(0, 255, 254)", "(0, 255, 254)"]


def test_encode_barely_green_rgba_png(raw_coded_rgba_barely_green_png, raw_image_rgba_png):
    """Tests encoding both valid RGBA .png images, with a valid 
    message in a color that is barely green.
    """
    new_image = sf.encode(raw_coded_rgba_barely_green_png, raw_image_rgba_png)
    data = []

    for i in su.image_reader(new_image):
        data.append(i)

    assert data == ["(0, 255, 255, 255)", "(0, 255, 254, 255)",
                    "(0, 255, 254, 255)", "(0, 255, 254, 255)"]


def test_encode_not_really_green_rgb_png(raw_coded_rgb_not_really_green_png, raw_image_rgb_png):
    """Tests encoding both valid RGB .png images, with a valid 
    message in an invalid shade of green.
    """
    new_image = sf.encode(raw_coded_rgb_not_really_green_png, raw_image_rgb_png)
    data = []

    for i in su.image_reader(new_image):
        data.append(i)

    assert data == ["(0, 255, 254)", "(0, 255, 254)",
                    "(0, 255, 254)", "(0, 255, 254)"]


def test_encode_not_realy_green_rgba_png(raw_coded_rgba_not_really_green_png, raw_image_rgba_png):
    """Tests encoding both valid RGBA .png images, with a valid 
    message in an invalid shade of green.
    """
    new_image = sf.encode(raw_coded_rgba_not_really_green_png, raw_image_rgba_png)
    data = []

    for i in su.image_reader(new_image):
        data.append(i)

    assert data == ["(0, 255, 254, 255)", "(0, 255, 254, 255)",
                    "(0, 255, 254, 255)", "(0, 255, 254, 255)"]


def test_encode_bright_blue_rgb_png(raw_coded_rgb_bright_blue_png, raw_image_rgb_png):
    """Tests encoding both valid RGB .png images, with a valid 
    message in bright blue.
    """
    new_image = sf.encode(raw_coded_rgb_bright_blue_png, raw_image_rgb_png)
    data = []

    for i in su.image_reader(new_image):
        data.append(i)

    assert data == ["(0, 255, 255)", "(0, 255, 254)",
                    "(0, 255, 254)", "(0, 255, 254)"]


def test_encode_bright_blue_rgba_png(raw_coded_rgba_bright_blue_png, raw_image_rgba_png):
    """Tests encoding both valid RGBA .png images, with a valid 
    message in bright blue.
    """
    new_image = sf.encode(raw_coded_rgba_bright_blue_png, raw_image_rgba_png)
    data = []

    for i in su.image_reader(new_image):
        data.append(i)

    assert data == ["(0, 255, 255, 255)", "(0, 255, 254, 255)",
                    "(0, 255, 254, 255)", "(0, 255, 254, 255)"]


def test_encode_definitely_blue_rgb_png(raw_coded_rgb_definitely_blue_png, raw_image_rgb_png):
    """Tests encoding both valid RGB .png images, with a valid 
    message in a color that is clearly blue.
    """
    new_image = sf.encode(raw_coded_rgb_definitely_blue_png, raw_image_rgb_png)
    data = []

    for i in su.image_reader(new_image):
        data.append(i)

    assert data == ["(0, 255, 255)", "(0, 255, 254)",
                    "(0, 255, 254)", "(0, 255, 254)"]


def test_encode_definitely_blue_rgba_png(raw_coded_rgba_definitely_blue_png, raw_image_rgba_png):
    """Tests encoding both valid RGBA .png images, with a valid 
    message in a color that is clearly blue.
    """
    new_image = sf.encode(raw_coded_rgba_definitely_blue_png, raw_image_rgba_png)
    data = []

    for i in su.image_reader(new_image):
        data.append(i)

    assert data == ["(0, 255, 255, 255)", "(0, 255, 254, 255)",
                    "(0, 255, 254, 255)", "(0, 255, 254, 255)"]


def test_encode_barely_blue_rgb_png(raw_coded_rgb_barely_blue_png, raw_image_rgb_png):
    """Tests encoding both valid RGB .png images, with a valid 
    message in a color that is barely blue.
    """
    new_image = sf.encode(raw_coded_rgb_barely_blue_png, raw_image_rgb_png)
    data = []

    for i in su.image_reader(new_image):
        data.append(i)

    assert data == ["(0, 255, 255)", "(0, 255, 254)",
                    "(0, 255, 254)", "(0, 255, 254)"]


def test_encode_barely_blue_rgba_png(raw_coded_rgba_barely_blue_png, raw_image_rgba_png):
    """Tests encoding both valid RGBA .png images, with a valid 
    message in a color that is barely blue.
    """
    new_image = sf.encode(raw_coded_rgba_barely_blue_png, raw_image_rgba_png)
    data = []

    for i in su.image_reader(new_image):
        data.append(i)

    assert data == ["(0, 255, 255, 255)", "(0, 255, 254, 255)",
                    "(0, 255, 254, 255)", "(0, 255, 254, 255)"]


def test_encode_not_really_blue_rgb_png(raw_coded_rgb_not_really_blue_png, raw_image_rgb_png):
    """Tests encoding both valid RGB .png images, with a valid 
    message in an invalid shade of blue.
    """
    new_image = sf.encode(raw_coded_rgb_not_really_blue_png, raw_image_rgb_png)
    data = []

    for i in su.image_reader(new_image):
        data.append(i)

    assert data == ["(0, 255, 254)", "(0, 255, 254)",
                    "(0, 255, 254)", "(0, 255, 254)"]


def test_encode_not_realy_blue_rgba_png(raw_coded_rgba_not_really_blue_png, raw_image_rgba_png):
    """Tests encoding both valid RGBA .png images, with a valid 
    message in an invalid shade of green.
    """
    new_image = sf.encode(raw_coded_rgba_not_really_blue_png, raw_image_rgba_png)
    data = []

    for i in su.image_reader(new_image):
        data.append(i)

    assert data == ["(0, 255, 254, 255)", "(0, 255, 254, 255)",
                    "(0, 255, 254, 255)", "(0, 255, 254, 255)"]


def test_encode_valid_rgb_coded_rgba_image_png(raw_coded_rgb_bright_red_png,
                                               raw_image_rgba_png):
    """Tests encoding both a valid RGB .png image inside a valid RGBA
    image.
    """
    new_image = sf.encode(raw_coded_rgb_bright_red_png, raw_image_rgba_png)
    data = []

    for i in su.image_reader(new_image):
        data.append(i)

    assert data == ["(0, 255, 255, 255)", "(0, 255, 254, 255)",
                    "(0, 255, 254, 255)", "(0, 255, 254, 255)"]


def test_encode_valid_rgba_coded_rgb_image_png(raw_coded_rgba_bright_red_png,
                                               raw_image_rgb_png):
    """Tests encoding both a valid RGBA .png image inside a valid RGB
    image.
    """
    new_image = sf.encode(raw_coded_rgba_bright_red_png, raw_image_rgb_png)
    data = []

    for i in su.image_reader(new_image):
        data.append(i)

    assert data == ["(0, 255, 255)", "(0, 255, 254)",
                    "(0, 255, 254)", "(0, 255, 254)"]


def test_encode_valid_rgb_smaller_png(raw_coded_smaller_rgb_png,
                                      raw_image_rgb_png):
    """Tests encoding a smaller RGB .png into a RGB .png image."""
    new_image = sf.encode(raw_coded_smaller_rgb_png, raw_image_rgb_png)
    data = []

    for i in su.image_reader(new_image):
        data.append(i)

    assert data == ["(0, 255, 255)", "(0, 255, 254)",
                    "(0, 255, 254)", "(0, 255, 254)"]


def test_encode_invalid_rgb_coded_jpeg(raw_image_rgb_jpeg, raw_image_rgb_png):
    """Tests encoding of an invalid RGB .jpeg image into a valid RGB
    .png image.
    """
    with pytest.raises(se.StegonosaurusIncorrectFormatError):
        sf.encode(raw_image_rgb_jpeg, raw_image_rgb_png)


def test_encode_invalid_rgb_image_jpeg(raw_coded_rgb_bright_red_png, raw_image_rgb_jpeg):
    """Tests encoding of a valid RGB .png image into an invalid RGB
    .jpeg image.
    """
    with pytest.raises(se.StegonosaurusIncorrectFormatError):
        sf.encode(raw_coded_rgb_bright_red_png, raw_image_rgb_jpeg)


def test_encode_invalid_l_coded_png(raw_image_l_png, raw_image_rgb_png):
    """Tests encoding an invalid single band .png image into an valid RGB .png
    image.
    """
    with pytest.raises(se.StegonosaurusIncorrectFormatError):
        sf.encode(raw_image_l_png, raw_image_rgb_png)


def test_encode_invalid_l_image_png(raw_coded_rgb_bright_red_png, raw_image_l_png):
    """Tests encoding an invalid single band .png image into an valid RGB .png
    image.
    """
    with pytest.raises(se.StegonosaurusIncorrectFormatError):
        sf.encode(raw_coded_rgb_bright_red_png, raw_image_l_png)


def test_encode_invalid_rgb_larger_png(raw_coded_larger_rgb_png,
                                       raw_image_rgb_png):
    """Tests encoding an invalid larger RGB .png image into a valid RGB
    .png image.
    """
    with pytest.raises(se.StegonosaurusIncorrectSizeError):
        sf.encode(raw_coded_larger_rgb_png, raw_image_rgb_png)


def test_encode_invalid_rgb_larger_x_png(raw_coded_larger_x_rgb_png,
                                         raw_image_rgb_png):
    """Tests encoding an invalid horizontally larger RGB .png image
    into a valid RGB .png image.
    """
    with pytest.raises(se.StegonosaurusIncorrectSizeError):
        sf.encode(raw_coded_larger_x_rgb_png, raw_image_rgb_png)


def test_encode_invalid_rgb_larger_y_png(raw_coded_larger_y_rgb_png,
                                         raw_image_rgb_png):
    """Tests encoding an invalid vertically larger RGB .png image into
    a valid RGB .png image.
    """
    with pytest.raises(se.StegonosaurusIncorrectSizeError):
        sf.encode(raw_coded_larger_y_rgb_png, raw_image_rgb_png)
