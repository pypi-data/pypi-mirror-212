

# Description

Un client Python pour l'API appeau, généré à partir du fichier de description suivant la spec OpenAPI 3.0.
Il nécessite une version de python >= 3.8, pour le typage des dictionnaires.

# Build & Install

Pour générer le module, suivre ce lien: https://docs.python.org/fr/3.8/distutils/introduction.html#distutils-simple-example

En synthèse:
```shell
python setup.py sdist # à la racine, voir https://docs.python.org/fr/3/distutils/sourcedist.html pour les formats d'archive possible
```
puis, par défaut dans /dist, et après extraction de l'archive, à la racine:
```shell
python setup.py install
```
# Exemple

```python
import sample.login_check_post
import sample.api_parcelles_get_collection
response = sample.login_check_post.login_check_post(host = 'http://appeau.api.vignevin-epicure.com', body_parameters = {"username": 'vitisexplorer',"password": 'Ajfkmdkp34'})
token = response.json()
print(token['token'])
parcelles = sample.api_parcelles_get_collection.api_parcelles_get_collection('http://appeau.api.vignevin-epicure.com', headers = {"Authorization": "Bearer " + token['token']})
print(parcelles.json())
```
