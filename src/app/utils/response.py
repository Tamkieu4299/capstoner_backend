def convert_response(status: bool, message: str, data: any):
    response = {"status": status, "message": message, "data": data}
    return response
