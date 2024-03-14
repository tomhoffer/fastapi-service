class JsonToXmlConversionException(Exception):
    """Exception raised when there is an error converting provided JSON to XML document.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Error converting provided JSON into XML!"):
        self.message = message
        super().__init__(self.message)


class XmlToJsonConversionException(Exception):
    """Exception raised when there is an error converting provided XML to JSON.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Error converting provided XML to JSON!"):
        self.message = message
        super().__init__(self.message)