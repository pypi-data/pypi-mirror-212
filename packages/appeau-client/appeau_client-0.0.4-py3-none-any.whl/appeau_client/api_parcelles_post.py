import requests
from typing import TypedDict, Any



class Required_Body_Parameters(TypedDict):
    pass

class Body_Parameters(Required_Body_Parameters, total = False):
    id: Any
    nom: Any
    latitude: Any
    longitude: Any
    parametres: Any
    pass

def api_parcelles_post(
    host


    , body_parameters: Body_Parameters
    ,
    # Optional body content
    optional_json_content = {}
    , headers = None
):
    final_path = "/api/parcelles"


    json_content = {
            **optional_json_content
            ,
            **body_parameters
        }

    response = requests.post(
        url = host + final_path,
        headers = headers
                ,
        json = json_content
    )

    return response