import requests
from typing import TypedDict, Any

class Path_Parameters(TypedDict):
    listParcellesId: Any
    pass



def api_parcellesdetails_listParcellesId_get_collection(
    host
    , path_parameters: Path_Parameters


    , headers = None
):
    # build paramatered path
    final_path = "/api/parcelles/details/{listParcellesId}".format(
        **path_parameters
        )


    response = requests.get(
        url = host + final_path,
        headers = headers
            )

    return response