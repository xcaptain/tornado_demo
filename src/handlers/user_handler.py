from handlers.base_handler import ApiBaseHandler


class UserSigninHandler(ApiBaseHandler):
    async def post(self):
        req = self.get_req_json()
        access_token = await self.user_service.login_user(req["email"], req["password"])
        self.data = {
            "access_token": access_token,
        }
        self.write_resp()


class UserRegisterHandler(ApiBaseHandler):
    async def post(self):
        req = self.get_req_json()
        access_token = await self.user_service.register_user(
            req["email"], req["password"]
        )
        self.data = {
            "access_token": access_token,
        }
        self.write_resp()
