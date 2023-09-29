import os
import azure.functions as func
from azure.cosmos import CosmosClient
import logging
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

url = "https://resumedev.documents.azure.com:443/"
key = os.environ.get('key')
client = CosmosClient(url, credential=key)
database = client.get_database_client('azureresume')
container = database.get_container_client('Counter')

# Define the HTTP-triggered function that will handle requests
@app.function_name(name="main")
@app.route(route="main")

def main(req: func.HttpRequest) -> func.HttpResponse:
    item_id = "1"  # ID of the item in CosmosDB
    item = container.read_item(item=item_id, partition_key=item_id)
    current_count = item['count']
    new_count = current_count + 1

    # Update the count in the database
    updated_item = {"id": item_id, "count": new_count}
    container.replace_item(item, updated_item)

    # Optionally, return the new count to the client
    return func.HttpResponse(json.dumps({"new_count": new_count}), mimetype="application/json")
    #return func.HttpResponseMessage(HttpStatusCodeOK, json.dumps({"new_count": new_count}), mimetype="application/json", encoding="UTF-8")

"""@app.function_name(name="GetResumeCount")
@app.route(route="GetResumeCount")
@app.cosmos_db_output(arg_name="outputDocument", database_name="azureresume", container_name="Counter", create_if_not_found=True, connection="CosmosDbConnectionString")
def GetResumeCount(req: func.HttpRequest, outputDocument: func.Out[func.Document]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    logging.info('Python Cosmos DB trigger function processed a request.')
    try:
        container = req.params.get('Counter')
        count = req.params.get('count')
        visit_item = container[count]
        current_count = visit_item.get('count', 0)
        visit_item['count'] = current_count + 1

        container.replace_item(item=visit_item, body=count)

        return func.HttpResponse(f"Visit Counted. Total visits: {visit_item}")

    except exceptions.CosmosResourceNotFoundError:
        # If the item does not exist, create it with a count of 1
        container.create_item(body={"id": "count", "count": 1})
        return func.HttpResponse("First visit counted. Total visits: 1", status_code=200)
    except Exception as e:
        return func.HttpResponse(f"An error occurred: {e}", status_code=500)


name = req.params.get('count')
    if not count:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('count')

    if name:
        outputDocument.set(func.Document.from_dict({"id": count}))
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )"""