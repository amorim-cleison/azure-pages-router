import azure.functions as func
from .router_func import RouterFunction


def main(req: func.HttpRequest) -> func.HttpResponse:
    return RouterFunction().process(req)
    