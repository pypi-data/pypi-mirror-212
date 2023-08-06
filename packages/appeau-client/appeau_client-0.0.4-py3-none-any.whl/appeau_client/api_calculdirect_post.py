import requests
from typing import TypedDict, Any




def api_calculdirect_post(
    host


    ,
    # Optional body content
    optional_json_content = {}
    , headers = None
):
    final_path = "/api/calcul/direct"


    json_content = {
            **optional_json_content
        }

    response = requests.post(
        url = host + final_path,
        headers = headers
                ,
        json = json_content
    )

    return response