class CustomError(Exception):
    status = 400
    message = None
    def __init__(self, message=None, status=None):
        if status is not None:
            self.status = status
        self.message = message
        super().__init__(self.message)

    @property
    def serialize(self) -> list[dict]:
        return [{'message': self.message}]