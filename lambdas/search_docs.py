import json
from utils import os_client, get_response, check_index_exists, ValidationError, IndexNotFoundException


def lambda_handler(event, context):
    try:
        print(event)
        index_name = event["pathParameters"]["index_name"]
        parsed_body = json.loads(event["body"])

        validate_payload(parsed_body)
        check_index_exists(index_name)

        query_dict = {
          "query": {
            "bool": {
                "minimum_should_match": 1,
                "should": [
                {
                  "multi_match": {
                    "query": parsed_body["text"],
                    "fields": ["title^5", "tags^4", "md_content^3", "created_by^2", "last_updated_by^2"]
                  }
                }
              ],
            }
          }
        }
        if parsed_body.get("category") and parsed_body.get("category").lower() != "all":
            query_dict["query"]["bool"]["filter"] = [
                {"term": { "category": parsed_body.get("category")}}
            ]

        response = os_client.search(
            body=query_dict, index=index_name
        )
        print(response)
        formatted_docs = []
        for doc in response["hits"]["hits"]:
            temp = doc["_source"]
            temp["doc_id"] = doc["_id"]
            formatted_docs.append(temp)

        result = {
            "count": response["hits"]["total"]["value"],
            "documents": formatted_docs
        }
        return get_response(
            status=200,
            message="",
            data=result,
        )
    except ValidationError as e:
        print(e)
        return get_response(
            status=400,
            message=str(e),
        )
    except IndexNotFoundException as e:
        print(e)
        return get_response(
            status=400,
            message=str(e),
        )
    except Exception as e:
        print(e)
        return get_response(
            status=400,
            message="error",
        )

def validate_payload(body):
    is_payload_valid = True
    is_payload_valid = is_payload_valid and "text" in body and body["text"]

    if not is_payload_valid:
        raise ValidationError("Must provide search text!")

