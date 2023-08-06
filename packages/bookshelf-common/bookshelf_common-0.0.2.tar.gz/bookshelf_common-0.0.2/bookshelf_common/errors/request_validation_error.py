from bookshelf_common.errors import CustomError
class RequestValidationError(CustomError):
    status = 400
    message = None
    errors = []
    def __init__(self, errors):
        self.message = 'Invalid request parameters'
        self.errors = errors
        super().__init__(self.message)

    @property
    def serialize(self) -> list[dict]:
        try:      
            errors = [{
                'field': x['loc'][1],
                'type': x['type'],
                'message': x['msg']
            } for x in self.errors if len(x['loc']) > 1 and x['loc'][1] is not None]
        except:
            errors = self.errors

        return errors if len(errors) > 0 else [{
            'field': 'all',
            'type': 'value_error.missing',
            'message': 'Required fields are not provided'
        }]

