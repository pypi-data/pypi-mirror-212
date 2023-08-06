import requests
from typing import TypedDict, Any

class Path_Parameters(TypedDict):
    id: Any
    pass



def api_parcelles_id_get(
    host
    , path_parameters: Path_Parameters


    , headers = None
):
    # build paramatered path
    final_path = "/api/parcelles/{id}".format(
        **path_parameters
        )


    response = requests.get(
        url = host + final_path,
        headers = headers
            )

    return response