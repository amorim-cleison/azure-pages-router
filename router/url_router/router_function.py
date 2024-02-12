import azure.functions as func
import json
import logging
from .constants import *
from .errors import *
from .error_handlers import *
from .error_messages import *
from .utils import *
from .url_mappings import *


class RouterFunction():

    def process(self, req: func.HttpRequest) -> func.HttpResponse:
        logging.info("Processing route request...")
        self.__log_request(req)

        try:
            # Read origin URL parameter:
            logging.info(
                f"Resolving origin URL ('{PARAM_ORIGIN_URL}') parameter...")
            param_value = get_request_param(PARAM_ORIGIN_URL, req)

            # Parse origin URL:
            logging.info(
                f"Origin URL ('{PARAM_ORIGIN_URL}') parameter: '{param_value}'")
            origin_url = parse_path_to_url(param_value)

            # Find target URL:
            logging.info(f"Resolving target URL...")
            target_url = find_target_url(origin_url.path, URL_MAPPINGS)

            # Process response:
            logging.info(f"Processing successful response...")
            response = self.__process_response(target_url)

        except Exception as e:
            logging.exception(e)
            logging.info(f"Processing error response...")
            response = self.__process_error_response(e)

        self.__log_response(response)
        return response

    def __process_response(self, target_url):
        return func.HttpResponse(headers={'Location': target_url},
                                 body=json.dumps(
                                     {'success': True, 'url': target_url}),
                                 mimetype="application/json",
                                 status_code=302)

    def __process_error_response(self, error):
        message = handler = None

        try:
            # Find matching code / error type:
            if error:
                message = str(error)
                error_type = type(error)
                handler = self.__get_error_handler(error_type)

            # If unable to resolve error handler:
            if handler is None:
                raise InternalServerError(ERROR_HANDLER_NOT_FOUND)

        except Exception as e:
            logging.warn(str(e))
            handler = self.__get_error_handler(type(InternalServerError))
            message = message if message else ERROR_RESPONSE_FALLBACK
        return self.__create_error_response(handler, message)

    def __get_error_handler(self, error_type):
        for handler in HTTP_CODES_HANDLERS:
            if error_type in handler.exceptions:
                return handler

    def __create_error_response(self, handler, message):
        params = {
            'success': False,
            'status': handler.status,
            'status_code': handler.status_code,
            'message': message
        }

        if handler.page is not None:
            # Load page and return HTML response:
            content = load_html_content(handler.page, params)
            mimetype = "text/html"
        else:
            # Return as JSON response:
            content = json.dumps(params)
            mimetype = "application/json"
        return func.HttpResponse(body=content, mimetype=mimetype, status_code=handler.status_code)

    def __log_request(self, req: func.HttpRequest):
        request_data = {
            "url": req.url,
            "method": req.method,
            "headers": map_to_str(req.headers),
            "params": map_to_str(req.params),
            "route_params": map_to_str(req.route_params),
            "body": req.get_body()
        }
        logging.info(f">>> Request received: {request_data}")

    def __log_response(self, resp: func.HttpResponse):
        response_data = {
            "status_code": resp.status_code,
            "mimetype": resp.mimetype,
            "headers": map_to_str(resp.headers),
            "charset": resp.charset,
            "body": resp.get_body()
        }
        logging.info(f"<<< Response returned: {response_data}")
