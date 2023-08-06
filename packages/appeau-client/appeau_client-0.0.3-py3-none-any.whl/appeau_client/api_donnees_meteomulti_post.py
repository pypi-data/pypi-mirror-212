import requests
from typing import TypedDict, Any




def api_donnees_meteomulti_post(
    host


    ,
    # Optional body content
    optional_json_content = {}
    , headers = None
):
    final_path = "/api/donnees_meteo/multi"


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