import datetime


class Response:
    def __init__(self,path, status_code, message, data=None):
        self.time = datetime.datetime.now().isoformat()
        self.path = path
        self.status_code = status_code
        self.message = message
        self.data = data

    def to_dict(self):
        return {
            "time": self.time,
            "path": self.path,
            "status_code": self.status_code,
            "message": self.message,
            "data": self.data,
        }
        
class IResponse:
    @staticmethod
    def init(path,status_code, message, data=None):
        return Response(path, status_code, message, data).to_dict()