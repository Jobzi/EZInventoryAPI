

class InvalidCredentialsError(Exception):

    def __init__(self, header: str, message: str = 'Could not validate credentials') -> None:
        self.message = message
        self.header = header
        super().__init__(self.message)


class NotEnoughPermissionsError(Exception):

    def __init__(self, header: str, message: str = 'Not enough permissions') -> None:
        self.header = header
        self.message = message
        super().__init__(self.message)
