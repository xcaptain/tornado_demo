from base.status_code import STATUS_MSG_MAP


class CommonException(Exception):
    def __init__(self, status, message=None):
        self.status = status
        self.message = message

    def __str__(self):
        err_msg = self.message or STATUS_MSG_MAP[self.status]
        return f"status={self.status}, err_msg={err_msg}"
