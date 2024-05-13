from fastapi import HTTPException, status


class NotFoundException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class InvalidFileType(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=detail)


class CommonInvalid(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=detail)


class InvalidDestination(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class InvalidInput(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=detail)
