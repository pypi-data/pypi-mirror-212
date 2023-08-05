from kfsd.apps.core.services.gateway.sso import SSO
from kfsd.apps.core.exceptions.api import KubefacetsAPIException
from kfsd.apps.core.common.logger import Logger, LogLevel

logger = Logger.getSingleton(__name__, LogLevel.DEBUG)


class TokenAuth(SSO):
    def __init__(self, request=None):
        SSO.__init__(self, request)

    def constructTokenResp(self, status, data, errors={}):
        return {
            "status": status,
            "data": data,
            "error": errors,
        }

    def readExceptionError(self, e):
        return {
            "detail": e.detail,
            "status_code": e.status_code,
            "default_code": e.default_code,
            "type": "error",
        }

    def getTokenUserInfo(self):
        try:
            payload = {
                "cookies": self.getDjangoRequest().getDjangoReqCookies().getAllCookies()
            }
            return self.verifyTokens(payload)
        except KubefacetsAPIException as e:
            errorJson = self.readExceptionError(e)
            logger.logWebRequestError(
                self.getDjangoRequest().getRequest(), errorJson, "error"
            )
            return self.constructTokenResp(False, {}, errorJson)
