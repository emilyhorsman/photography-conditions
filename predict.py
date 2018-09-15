import os
import getpass
import requests

authorization_path = os.path.expanduser('~/.photographyconditions')

def get_authorization_from_fs():
    if not os.path.isfile(authorization_path):
        return None

    with open(authorization_path, 'r') as f:
        return f.read()

def get_authorization_from_login():
    username = input('Username: ')
    password = getpass.getpass()

    auth_response = requests.post(
        'https://sunburst.sunsetwx.com/v1/login',
        auth=(username, password),
        params=dict(grant_type='password'),
    )
    data = auth_response.json()
    print(data)
    access_token = data['token']
    token_type = 'Bearer'
    authorization = '{} {}'.format(token_type, access_token)
    with open(authorization_path, 'w') as f:
        f.write(authorization)
    return authorization

authorization = get_authorization_from_fs()
if authorization is None:
    authorization = get_authorization_from_login()

prediction_response = requests.get(
    'https://sunburst.sunsetwx.com/v1/quality',
    params=dict(geo='43.2740851,-79.8994183'),
    headers={'Authorization': authorization}
)
prediction_data = prediction_response.json()
sunset_prediction = next(filter(
    lambda f: f['properties']['type'] == 'Sunset',
    prediction_data['features']
))
print('Quality Prediction: {} ({}%)'.format(
    sunset_prediction['properties']['quality'],
    sunset_prediction['properties']['quality_percent'])
)