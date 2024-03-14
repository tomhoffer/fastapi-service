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


class DbRecordNotFoundException(Exception):
    """Exception raised when the specified record does not exist in the database

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="DB record not found!"):
        self.message = message
        super().__init__(self.message)


class DbUnableToInsertRowException(Exception):
    """Exception raised when the specified record could not be insrted into the database

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="DB record could not be inserted!"):
        self.message = message
        super().__init__(self.message)
