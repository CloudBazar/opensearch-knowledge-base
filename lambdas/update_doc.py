import time
import json
from utils import os_client, get_response, check_index_exists, ValidationError, IndexNotFoundException
from opensearchpy import NotFoundError


def lambda_handler(event, context):
    try:
        print(event)
        index_name = event["pathParameters"]["index_name"]
        doc_id = event["pathParameters"]["doc_id"]

        parsed_body = json.loads(event["body"])
        validate_payload(parsed_body)
        check_index_exists(index_name)

        last_updated_by = parsed_body["last_updated_by"]
        last_updated_at_ms = int(time.time() * 1000)
        form_data = {
            "category": parsed_body["category"],
            "title": parsed_body["title"],
            "tags": parsed_body["tags"],
            "md_content": parsed_body["md_content"],
            "last_updated_by": last_updated_by,
            "last_updated_at_ms": last_updated_at_ms,
        }

        body = {"doc": form_data}
        response = os_client.update(
            index=index_name,
            id=doc_id,
            body=body,
            _source=True,
        )
        print(response)

        return get_response(
            status=200,
            message=f"Document (ID: {response.get('_id')}) updated successfully",
            data="",
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
    except NotFoundError as e:
        print(e)
        return get_response(
            status=400,
            message="Document not found!",
        )
    except Exception as e:
        print(e)
        return get_response(
            status=400,
            message="error",
        )

def validate_payload(body):
    is_payload_valid = True
    is_payload_valid = is_payload_valid and "category" in body and body["category"]
    is_payload_valid = is_payload_valid and "title" in body and body["title"]
    is_payload_valid = is_payload_valid and "tags" in body and body["tags"]
    is_payload_valid = is_payload_valid and "md_content" in body and body["md_content"]
    is_payload_valid = is_payload_valid and "last_updated_by" in body and body["last_updated_by"]

    if not is_payload_valid:
        raise ValidationError("Must provide all values!")

