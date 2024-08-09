class ShopsAppException(Exception):
    """
    Custom exception class for ShopsApp
    Can be used to raise exceptions in the application of type:
    - Not Found Exception
    - Bad Request Exception
    - General Exception
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class ShopsAppUnAuthorizedException(Exception):
    """
    Custom exception class for ShopsApp Unauthorized Exception
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class ShopsAppDeletionFailException(Exception):
    """
    Custom exception class for ShopsApp Deletion Fail Exception
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class ShopsAppAlreadyExistsException(Exception):
    """
    Custom exception class for ShopsApp Already Exists Exception
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
