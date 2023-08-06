import requests
from typing import TypedDict, Any

class Path_Parameters(TypedDict):
    parcelleId: Any
    pass



def api_date_calcul_parcelleId_get(
    host
    , path_parameters: Path_Parameters


    , headers = None
):
    # build paramatered path
    final_path = "/api/date_calcul/{parcelleId}".format(
        **path_parameters
        )


    response = requests.get(
        url = host + final_path,
        headers = headers
            )

    return response