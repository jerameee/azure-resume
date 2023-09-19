import logging
import json
import azure.functions as func

def main(req: func.HttpRequest, inputDocument: func.DocumentList, outputDocument: func.Out[func.Document]) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    id_value = req.params.get('id')
    logging.info(f"Received id_value: {id_value}")

    if not id_value:
        logging.error("Missing id parameter")
        return func.HttpResponse("Missing id parameter", status_code=400)

    if not inputDocument:
        logging.error("No document found in CosmosDB")
        return func.HttpResponse("No document found", status_code=404)

    doc = inputDocument[0]
    logging.info(f"Fetched document: {doc}")

    new_count = doc['count'] + 1
    logging.info(f"New count value: {new_count}")

    outputDocument.set(func.Document.from_dict({
        "id": doc["id"],
        "count": new_count
    }))

    logging.info("Processed document with id: %s", doc['id'])

    return func.HttpResponse(
        json.dumps({
            "success": True,
            "id": doc["id"],
            "count": new_count
        }),
        mimetype="application/json"
    )
