import logging
import json
import azure.functions as func

def main(req: func.HttpRequest, inputDocument: func.DocumentList, outputDocument: func.Out[func.Document]) -> func.HttpResponse:
    if not inputDocument:
        return func.HttpResponse("No document found", status_code=404)

    # Taking th first document if it exists
    doc = inputDocument[0]

    # Incrementing the counter
    new_count = doc.get('count', 0) + 1
    doc['count'] = new_count

    # Send modified document to output binding to be saved in CosmosDB
    outputDocument.set(func.document.from_dict(doc))

    return func.HttpResponse(
        json.dumps({
            "success": True,
            "id": doc["id"],
            "count": new_count
        }),
        mimetype="application/json"
    )