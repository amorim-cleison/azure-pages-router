import logging
import azure.functions as func
from .router_helper import find_route


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Processing route request...")

    try:
        originUrl = None

        # # GET:
        # originUrl = req.params.get('originUrl')

        if not originUrl:
            # POST:
            try:
                req_body = req.get_json()
            except ValueError:
                pass
            else:
                originUrl = req_body.get('originUrl')

        logging.info(f"Processing target route for origin '{originUrl}'...")
        targetUrl = find_route(originUrl)

        if not targetUrl:
            logging.error("Could not find route for the URL requested")
            return func.HttpResponse("Target page not found", status_code=404)

        return func.HttpResponse(targetUrl,
                                 headers={'Location': targetUrl},
                                 status_code=302)
    except Exception as e:
        logging.exception(e)
        return func.HttpResponse("Failed to resolve target URL",
                                 status_code=500)
