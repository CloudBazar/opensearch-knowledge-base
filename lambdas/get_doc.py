from utils import os_client, get_response, check_index_exists, IndexNotFoundException


def lambda_handler(event, context):
    try:
        print(event)
        index_name = event["pathParameters"]["index_name"]
        doc_id = event["pathParameters"]["doc_id"]

        check_index_exists(index_name)

        response = os_client.get(
            index=index_name,
            id=doc_id,
        )
        print(response)
        temp = response["_source"]
        temp["doc_id"] = response["_id"]

        return get_response(
            status=200,
            message="",
            data=temp,
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

