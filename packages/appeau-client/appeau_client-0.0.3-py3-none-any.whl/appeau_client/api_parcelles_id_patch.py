import requests
from typing import TypedDict, Any

class Path_Parameters(TypedDict):
    id: Any
    pass



def api_parcelles_id_patch(
    host
    , path_parameters: Path_Parameters


    ,
    # Optional body content
    optional_json_content = {}
    , headers = None
):
    # build paramatered path
    final_path = "/api/parcelles/{id}".format(
        **path_parameters
        )


    json_content = {
            **optional_json_content
        }

    response = requests.patch(
        url = host + final_path,
        headers = headers
                ,
        json = json_content
    )

    return response