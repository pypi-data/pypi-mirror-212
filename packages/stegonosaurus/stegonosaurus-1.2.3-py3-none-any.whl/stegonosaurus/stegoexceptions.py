"""Custom exceptions made for this library."""


class StegonosaurusIncorrectFormatError(Exception):
    """Raised when a function receives a file that isn't a .PNG multiband image."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class StegonosaurusIncorrectSizeError(Exception):
    """Raised when the image with the coded message is larger than the image
    where the message will be hidden.
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class StegonosaurusInvalidDecodeModeError(Exception):
    """Raised when an invalid decode mode is provided."""
    def __init__(self, message):
        self.message = message
        self.message = message
        super().__init__(self.message)
