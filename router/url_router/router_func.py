import logging
import azure.functions as func
from .router_utils import find_route
from urllib.parse import urlparse

ORIGIN_URL_PARAM = 'originUrl'


class RouterFunction():

    def process(self, req: func.HttpRequest) -> func.HttpResponse:
        logging.info("Processing route request...")
        originUrl = None
        targetUrl = None
        
        try:
            # Read origin URL parameter:
            read_methods = [self.__read_as_get, self.__read_as_post]
            
            for method_fn in read_methods:
                originUrl = method_fn(req)

                if originUrl:
                    originUrl = self.__parse_to_url(originUrl)
                    break
            
            # Find target URL:
            if originUrl:
                logging.info(f"Parameter '{ORIGIN_URL_PARAM}' found: {originUrl}")
                logging.info(f"Processing target route...")
                targetUrl = find_route(originUrl)
            else:
                raise Exception(f"Parameter '{ORIGIN_URL_PARAM}' was not provided")

            # Process response:
            return self.__process_response(targetUrl)

        except Exception as e:
            logging.exception(e)
            return self.__process_response(targetUrl, e)


    def __parse_to_url(self, originUrl):
        try:
            return urlparse(originUrl)
        except Exception as e:
            raise Exception(f"Invalid URL provided in the '{ORIGIN_URL_PARAM}' parameter") from e


    def __read_as_get(self, req):
        logging.info(f"Reading '{ORIGIN_URL_PARAM}' as GET parameter...")
        return req.params.get(ORIGIN_URL_PARAM)


    def __read_as_post(self, req):
        logging.info(f"Trying to read '{ORIGIN_URL_PARAM}' from POST parameters...")
        
        try:
            req_body = req.get_json()
        except ValueError as e:
            pass
        else:
            originUrl = req_body.get(ORIGIN_URL_PARAM)
        return originUrl


    def __process_response(self, targetUrl, error=None):
        if error:
            return func.HttpResponse(f"Failed to resolve target URL: {error}", status_code=500)
        
        elif targetUrl:
            # Valid response:
            return func.HttpResponse(targetUrl, headers={'Location': targetUrl}, status_code=302)

        else:
            return func.HttpResponse("Could not find route for the URL requested", status_code=404)
