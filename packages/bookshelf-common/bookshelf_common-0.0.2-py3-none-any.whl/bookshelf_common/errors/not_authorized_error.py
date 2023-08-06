from bookshelf_common.errors import CustomError
class NotAuthorizedError(CustomError):
    status = 401
    message = None
    def __init__(self):
        self.message = 'Not Authorized'
        super().__init__(self.message)