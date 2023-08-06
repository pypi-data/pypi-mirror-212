from kfsd.apps.core.services.gateway.sso import SSO
from kfsd.apps.core.exceptions.api import KubefacetsAPIException
from kfsd.apps.core.common.logger import Logger, LogLevel

logger = Logger.getSingleton(__name__, LogLevel.DEBUG)


class TokenAuth(SSO):
    def __init__(self, request=None):
        SSO.__init__(self, request)

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
            return self.constructGatewayResp(False, {}, errorJson)
