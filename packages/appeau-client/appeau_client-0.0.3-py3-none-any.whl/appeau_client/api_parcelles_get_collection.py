import requests
from typing import TypedDict, Any




def api_parcelles_get_collection(
    host


    , headers = None
):
    final_path = "/api/parcelles"


    response = requests.get(
        url = host + final_path,
        headers = headers
            )

    return response