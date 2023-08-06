import requests
from typing import TypedDict, Any




def api_parcellesattente_get_collection(
    host


    , headers = None
):
    final_path = "/api/parcelles/attente"


    response = requests.get(
        url = host + final_path,
        headers = headers
            )

    return response