import getpass
import iso8601
import os
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

def get_prediction_response(authorization):
    return requests.get(
        'https://sunburst.sunsetwx.com/v1/quality',
        params=dict(geo='43.2740851,-79.8994183'),
        headers={'Authorization': authorization}
    )

prediction_response = get_prediction_response(authorization)
if prediction_response.status_code != 200:
    authorization = get_authorization_from_login()
    prediction_response = get_prediction_response(authorization)


def print_prediction(prediction_data):
    if prediction_data.get('type') != 'FeatureCollection':
        return

    features = prediction_data.get('features', [])
    for feature in features:
        props = feature['properties']
        print('{} prediction updated at {}: {} ({}%)'.format(
            props['type'],
            iso8601.parse_date(props['last_updated']).strftime('%-I:%M%p'),
            props['quality'],
            props['quality_percent'],
        ))

print_prediction(prediction_response.json())
