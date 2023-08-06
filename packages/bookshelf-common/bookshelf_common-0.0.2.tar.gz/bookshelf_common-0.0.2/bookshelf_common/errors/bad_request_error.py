from bookshelf_common.errors import CustomError
class BadRequestError(CustomError):
    status = 400
    message = None
    
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)