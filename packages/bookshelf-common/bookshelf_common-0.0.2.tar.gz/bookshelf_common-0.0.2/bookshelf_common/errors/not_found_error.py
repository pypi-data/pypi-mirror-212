from bookshelf_common.errors import CustomError
class NotFoundError(CustomError):
    status = 404
    message = 'Not found'

    def __init__(self):
        self.message = 'Not found'
        super().__init__(self.message)