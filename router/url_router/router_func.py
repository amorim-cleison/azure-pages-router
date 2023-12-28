import logging
import azure.functions as func
from .router_utils import find_route
from urllib.parse import urlparse

ORIGIN_URL_PARAM = 'originUrl'


class RouterFunction():

    def process(self, req: func.HttpRequest) -> func.HttpResponse:
        logging.info("Processing route request...")
        targetUrl = None
        
        # Log request:
        self.__log_request(req)

        try:
            # Read origin URL parameter:
            originUrl = self.__read_origin_url(req)

            if originUrl is None:
                raise MissingArgumentError(f"Parameter '{ORIGIN_URL_PARAM}' was not provided")
            
            # Find target URL:
            logging.info(f"Parameter '{ORIGIN_URL_PARAM}' found: {originUrl}")
            logging.info(f"Processing target route...")
            targetUrl = find_route(originUrl)

            # Check if a route was found:
            if targetUrl is None:
                raise RouteNotFoundError("No route URL found for the path informed")

            # Process response:
            response = self.__process_response(targetUrl)

        except Exception as e:
            logging.exception(e)
            response = self.__process_error_response(e)

        # Log response:
        self.__log_response(response)
        return response


    def __parse_to_url(self, originUrl):
        try:
            return urlparse(originUrl)
        except Exception as e:
            raise InvalidArgumentError(f"Invalid URL provided in the '{ORIGIN_URL_PARAM}' parameter") from e


    def __read_origin_url(self, req):
        originUrl = None
        read_methods = [self.__read_as_get, self.__read_as_post]
            
        for method_fn in read_methods:
            originUrl = method_fn(req)

            if originUrl:
                originUrl = self.__parse_to_url(originUrl)
                break
        return originUrl
        

    def __read_as_get(self, req):
        logging.info(f"Reading '{ORIGIN_URL_PARAM}' as GET parameter...")
        return req.params.get(ORIGIN_URL_PARAM)


    def __read_as_post(self, req):
        originUrl = None
        logging.info(f"Trying to read '{ORIGIN_URL_PARAM}' from POST parameters...")
        
        try:
            req_body = req.get_json()
        except ValueError as e:
            pass
        else:
            originUrl = req_body.get(ORIGIN_URL_PARAM)
        return originUrl


    def __process_response(self, targetUrl):
        return func.HttpResponse(targetUrl, headers={'Location': targetUrl}, status_code=302)


    def __process_error_response(self, error):
        response = None

        if error:
            error_codes_types = {
                400: [MissingArgumentError, InvalidArgumentError],
                404: [RouteNotFoundError]
            }
            error_type = type(error)

            # Find matching code / error type:
            for code, types in error_codes_types.items():
                if error_type in types:
                    response = func.HttpResponse(str(error), status_code=400)

        # If not matched, returns default error response:
        if response is None:
            msg = "Failed to resolve target URL"
            msg = f"{msg}: {error}" if error else msg
            response = func.HttpResponse(msg, status_code=500)
        
        return response


    def __log_request(self, req: func.HttpRequest):
        request_data = {
            "url": req.url,
            "method": req.method,
            "headers": self.__map_to_str(req.headers),
            "params": self.__map_to_str(req.params),
            "route_params": self.__map_to_str(req.route_params),
            "body": req.get_body()
        }
        logging.info(f">>> Request received: {request_data}")


    def __log_response(self, resp: func.HttpResponse):
        response_data = {
            "status_code": resp.status_code,
            "mimetype": resp.mimetype,
            "headers": self.__map_to_str(resp.headers),
            "charset": resp.charset,
            "body": resp.get_body()
        }
        logging.info(f"<<< Response returned: {response_data}")


    def __map_to_str(self, m):
        return [ f"{k}: {v}" for k, v in m.items() ]
    


class InvalidArgumentError(ValueError):
    pass

class MissingArgumentError(ValueError):
    pass

class RouteNotFoundError(Exception):
    pass