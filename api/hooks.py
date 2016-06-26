import logging

def oAuthUserRequired(handler_method):
    def checkUser(self):
        api_key = ["abc-123"]
        try:
            # ADD CODE HERE
            authorized = True
            handler_method(self, authorized)
        except Exception as e:
            logging.info(e)
            self.response.set_status(401)
            BaseHandler.server_resp(self, 401, 'Not authorized to use Rics Code test API', {})
    return checkUser