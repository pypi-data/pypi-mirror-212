import requests
from typing import TypedDict, Any

class Path_Parameters(TypedDict):
    listParcellesId: Any
    dateDebut: Any
    dateFin: Any
    pass



def api_parcellesmulti_listParcellesIdresultat_dateDebut_dateFin_get_collection(
    host
    , path_parameters: Path_Parameters


    , headers = None
):
    # build paramatered path
    final_path = "/api/parcelles/multi/{listParcellesId}/resultat/{dateDebut}/{dateFin}".format(
        **path_parameters
        )


    response = requests.get(
        url = host + final_path,
        headers = headers
            )

    return response