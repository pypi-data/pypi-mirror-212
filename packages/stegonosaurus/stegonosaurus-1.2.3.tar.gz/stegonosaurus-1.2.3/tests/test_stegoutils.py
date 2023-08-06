"""Test the utils for the Stegonosaurus library"""
from stegonosaurus import stegoutils as su


# Image reader tests:
def test_image_reader(raw_image_rgb_png):
    """Tests the image reader, generator used in the inspect
    function.
    """
    data = []

    for i in su.image_reader(raw_image_rgb_png):
        data.append(i)

    assert data == ["(0, 255, 255)", "(0, 255, 255)",
                    "(0, 255, 255)", "(0, 255, 255)"]


# Format validation tests:
def test_validate_format_png_rgb(raw_image_rgb_png):
    """Test the validation of a .png RGB image."""
    assert su.validate_image_format(raw_image_rgb_png)


def test_validate_format_png_rgba(raw_image_rgba_png):
    """Test the validation of a .png RGBA image."""
    assert su.validate_image_format(raw_image_rgba_png)


def test_validate_format_l_rgb(raw_image_l_png):
    """Test the validation of a .png single-band image."""
    assert not su.validate_image_format(raw_image_l_png)


def test_validate_format_jpeg_rgb(raw_image_rgb_jpeg):
    """Test the validation of a .jpeg RGB image."""
    assert not su.validate_image_format(raw_image_rgb_jpeg)


def test_validate_format_jpeg_rgba(raw_image_rgba_jpeg):
    """Test the validation of a .jpeg RGB image."""
    assert not su.validate_image_format(raw_image_rgba_jpeg)


# Size validation tests:
def test_same_size_images(raw_coded_rgb_bright_red_png, raw_image_rgb_png):
    """Test the validation of same size .png RGB images."""
    assert su.validate_images_size(raw_coded_rgb_bright_red_png, raw_image_rgb_png)


def test_smaller_coded_image(raw_coded_smaller_rgb_png, raw_image_rgb_png):
    """Test the validation of .png RGB images where the coded one is smaller."""
    assert su.validate_images_size(raw_coded_smaller_rgb_png,
                                   raw_image_rgb_png)


def test_larger_x_coded_image(raw_coded_larger_x_rgb_png, raw_image_rgb_png):
    """Test the validation of a horizontally larger .png RGB coded image."""
    assert not su.validate_images_size(raw_coded_larger_x_rgb_png,
                                       raw_image_rgb_png)


def test_larger_y_coded_image(raw_coded_larger_y_rgb_png, raw_image_rgb_png):
    """Test the validation of a vertically larger .png RGB coded image."""
    assert not su.validate_images_size(raw_coded_larger_y_rgb_png,
                                       raw_image_rgb_png)


def test_larger_coded_image(raw_coded_larger_rgb_png, raw_image_rgb_png):
    """Test the validation of a larger .png RGB coded image."""
    assert not su.validate_images_size(raw_coded_larger_rgb_png,
                                       raw_image_rgb_png)


# Decode mode validation tests:
def test_validate_decode_mode_lower_t():
    """Tests validation when the decode mode is t."""
    assert su.validate_decode_mode("t")


def test_validate_decode_mode_lower_b():
    """Tests validation when the decode mode is b."""
    assert su.validate_decode_mode("b")


def test_validate_decode_mode_upper_t():
    """Tests validation when the decode mode is T."""
    assert su.validate_decode_mode("T")


def test_validate_decode_mode_upper_b():
    """Tests validation when the decode mode is B."""
    assert su.validate_decode_mode("B")


def test_validate_decode_mode_invalid_string():
    """Tests validation when decode mode is not valid."""
    assert not su.validate_decode_mode("CAKE")


def test_validate_decode_mode_nonstring():
    """Tests validation when decode mode is not a string."""
    assert not su.validate_decode_mode(3)


# Image flattening tests:
def test_flatten_rgb_image(raw_image_rgb_png):
    """Test the flatenning of an RGB .png image."""
    flat_image = su.flatten_image(raw_image_rgb_png)
    data = []

    for i in su.image_reader(flat_image):
        data.append(i)

    assert data == ["(0, 255, 254)", "(0, 255, 254)",
                    "(0, 255, 254)", "(0, 255, 254)"]


def test_flatten_rgba_image(raw_image_rgba_png):
    """Test the flatenning of an RGBA .png image."""
    flat_image = su.flatten_image(raw_image_rgba_png)
    data = []

    for i in su.image_reader(flat_image):
        data.append(i)

    assert data == ["(0, 255, 254, 255)", "(0, 255, 254, 255)",
                    "(0, 255, 254, 255)", "(0, 255, 254, 255)"]


def test_flatten_code_rgb_bright_image(raw_coded_rgb_bright_red_png):
    """Tests the falettening of an RGB .png coded image with bright text."""
    flat_coded = su.flatten_coded(raw_coded_rgb_bright_red_png)
    data = []

    for i in su.image_reader(flat_coded):
        data.append(i)

    assert data == ["(255, 0, 0)", "(0, 0, 0)", "(0, 0, 0)", "(0, 0, 0)"]


def test_flatten_code_rgba_bright_image(raw_coded_rgba_bright_red_png):
    """Tests the falettening of an RGBA .png coded image with bright text."""
    flat_coded = su.flatten_coded(raw_coded_rgba_bright_red_png)
    data = []

    for i in su.image_reader(flat_coded):
        data.append(i)

    assert data == ["(255, 0, 0, 255)", "(0, 0, 0, 255)",
                    "(0, 0, 0, 255)", "(0, 0, 0, 255)"]


def test_flatten_code_rgb_barely_image(raw_coded_rgb_barely_red_png):
    """Tests the falettening of an RGB .png coded image with dark acceptable text."""
    flat_coded = su.flatten_coded(raw_coded_rgb_barely_red_png)
    data = []

    for i in su.image_reader(flat_coded):
        data.append(i)

    assert data == ["(255, 0, 0)", "(0, 0, 0)", "(0, 0, 0)", "(0, 0, 0)"]


def test_flatten_code_rgba_barely_image(raw_coded_rgba_barely_red_png):
    """Tests the falettening of an RGBA .png coded image with dark acceptable text."""
    flat_coded = su.flatten_coded(raw_coded_rgba_barely_red_png)
    data = []

    for i in su.image_reader(flat_coded):
        data.append(i)

    assert data == ["(255, 0, 0, 255)", "(0, 0, 0, 255)",
                    "(0, 0, 0, 255)", "(0, 0, 0, 255)"]


def test_flatten_code_rgb_definitely_image(raw_coded_rgb_definitely_red_png):
    """Tests the falettening of an RGB .png coded image with clearly colored text."""
    flat_coded = su.flatten_coded(raw_coded_rgb_definitely_red_png)
    data = []

    for i in su.image_reader(flat_coded):
        data.append(i)

    assert data == ["(255, 0, 0)", "(0, 0, 0)", "(0, 0, 0)", "(0, 0, 0)"]


def test_flatten_code_rgba_definitely_image(raw_coded_rgba_definitely_red_png):
    """Tests the falettening of an RGBA .png coded image with clearly colored text."""
    flat_coded = su.flatten_coded(raw_coded_rgba_definitely_red_png)
    data = []

    for i in su.image_reader(flat_coded):
        data.append(i)

    assert data == ["(255, 0, 0, 255)", "(0, 0, 0, 255)",
                    "(0, 0, 0, 255)", "(0, 0, 0, 255)"]


def test_flatten_code_rgb_not_really_image(raw_coded_rgb_not_really_red_png):
    """Tests the falettening of an RGB .png coded image with non encodable text."""
    flat_coded = su.flatten_coded(raw_coded_rgb_not_really_red_png)
    data = []

    for i in su.image_reader(flat_coded):
        data.append(i)

    assert data == ["(0, 0, 0)", "(0, 0, 0)", "(0, 0, 0)", "(0, 0, 0)"]


def test_flatten_code_rgba_not_really_image(raw_coded_rgba_not_really_red_png):
    """Tests the falettening of an RGBA .png coded image with non encodable text."""
    flat_coded = su.flatten_coded(raw_coded_rgba_not_really_red_png)
    data = []

    for i in su.image_reader(flat_coded):
        data.append(i)

    assert data == ["(0, 0, 0, 255)", "(0, 0, 0, 255)",
                    "(0, 0, 0, 255)", "(0, 0, 0, 255)"]


# Pixel coloring validation tests:
def test_is_colored_red(barely_red_pixel, definitely_red_pixel, bright_red_pixel,
                        not_really_red_pixel):
    """Tests the validation pixels of different shades of red."""
    results = [
        su.is_colored(barely_red_pixel),
        su.is_colored(definitely_red_pixel),
        su.is_colored(bright_red_pixel),
        su.is_colored(not_really_red_pixel)
    ]
    assert results == [True, True, True, False]


def test_is_colored_green(barely_green_pixel, definitely_green_pixel, bright_green_pixel,
                          not_really_green_pixel):
    """Tests the validation pixels of different shades of green."""
    results = [
        su.is_colored(barely_green_pixel),
        su.is_colored(definitely_green_pixel),
        su.is_colored(bright_green_pixel),
        su.is_colored(not_really_green_pixel)
    ]
    assert results == [True, True, True, False]


def test_is_colored_blue(barely_blue_pixel, definitely_blue_pixel, bright_blue_pixel,
                         not_really_blue_pixel):
    """Tests the validation pixels of different shades of blue."""
    results = [
        su.is_colored(barely_blue_pixel),
        su.is_colored(definitely_blue_pixel),
        su.is_colored(bright_blue_pixel),
        su.is_colored(not_really_blue_pixel)
    ]
    assert results == [True, True, True, False]


def test_is_colored_black(soft_black_pixel, hard_black_pixel):
    """Tests the validation pixels of different invalid shades of black."""
    result = [
        su.is_colored(soft_black_pixel),
        su.is_colored(hard_black_pixel)
    ]

    assert result == [False, False]
