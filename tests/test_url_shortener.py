import json
import pytest
from url_shortener import app 

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_encrypt_decrypt_flow(client):
    long_url = 'https://www.google.com'
    encrypt_response = client.post('/encrypt', json={'long_url': long_url})
    assert encrypt_response.status_code == 200
    encrypted_data = json.loads(encrypt_response.data)
    assert 'short_url' in encrypted_data

    short_url = encrypted_data['short_url']

    decrypt_response = client.get(f'/decrypt/{short_url}', follow_redirects=True)
    assert decrypt_response.status_code == 200

    decrypted_data = json.loads(decrypt_response.data)

    assert 'long_url' in decrypted_data
    assert decrypted_data['long_url'] == long_url

def test_nonexistent_short_url(client):
    nonexistent_short_url = 'nonexistent_short_url'

    decrypt_response = client.get(f'/decrypt/{nonexistent_short_url}')
    assert decrypt_response.status_code == 404

    error_data = json.loads(decrypt_response.data)

    assert 'error' in error_data

# Add more test cases as needed

if __name__ == '__main__':
    pytest.main()