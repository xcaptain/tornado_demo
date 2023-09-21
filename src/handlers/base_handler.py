import http
import json
import logging
from typing import Any

import tornado
import tornado.escape
from tornado import httputil
from tornado.web import HTTPError, RequestHandler

from base.status_code import CONTENT_TYPE, STATUS_ERROR, STATUS_MSG_MAP, STATUS_UNKNOWN
from common.common_exception import CommonException
from services.user_service import UserService


class ApiBaseHandler(RequestHandler):
    """
    1, subclass set status and data,
    2, call write_resp
    """

    def __init__(self, application, request: httputil.HTTPServerRequest) -> None:
        super(ApiBaseHandler, self).__init__(application, request)
        self._logging = logging.getLogger(self.__class__.__name__)
        self.req_json = None
        self.status = STATUS_ERROR
        self.message = None
        self.data = None
        self.user_service: UserService = application.user_service

    def msg_format(self, status, data=None):
        msg = self.message if self.message else STATUS_MSG_MAP.get(status, "")
        temp = {"status": status, "msg": msg}

        if data or data == []:
            temp["data"] = data

        if not msg:
            logging.warning("msg_format msg is not define temp=%s", temp)

        return temp

    def write_pure_json(self, content):
        self.set_header("Content-Type", CONTENT_TYPE)
        self.finish(json.dumps(content))

    def write_resp(self):
        resp = self.msg_format(self.status, self.data)
        resp_str = json.dumps(resp)
        self.set_header("Content-Type", CONTENT_TYPE)
        self.finish(resp_str)

    def write_error(self, status_code: int, **kwargs: Any):
        if "exc_info" in kwargs:
            ex_type, ex, trace_back = kwargs["exc_info"]
            if isinstance(ex, CommonException):
                logging.exception(f"known error: {ex}")
                self.status = ex.status
                self.message = ex.message
                self.set_status(http.HTTPStatus.BAD_REQUEST)
                self.write_resp()
                return
            elif not isinstance(ex, HTTPError):
                # server internal error
                logging.exception(f"unknown error: {ex}")
                self.status = STATUS_UNKNOWN
                self.set_status(http.HTTPStatus.INTERNAL_SERVER_ERROR)
                self.write_resp()
                return

        self.set_status(ex.status_code)
        self.status = status_code
        self.message = self._reason
        self.write_resp()

    def get_req_json(self):
        if self.req_json is not None:
            return self.req_json
        else:
            if self.request.body:
                self.req_json = tornado.escape.json_decode(self.request.body)
            else:
                self.req_json = {}
            return self.req_json
