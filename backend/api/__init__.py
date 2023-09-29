import logging
import azure.functions as func
from .function_app import main

def run(req: func.HttpRequest) -> func.HttpResponse:
    return main(req)
