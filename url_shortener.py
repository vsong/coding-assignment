from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from repositories.url_repository import URLRepository

import hashlib

app = Flask(__name__)
limiter = Limiter(
    key_func=get_remote_address, 
    app=app, 
    default_limits=["2 per second"], 
    storage_uri="memory://"
)

url_repo = URLRepository()

def generate_short_url(long_url):
    hash_object = hashlib.sha256(long_url.encode())
    hex_dig = hash_object.hexdigest()
    return hex_dig[:8]

@limiter.limit("2 per second")
@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.get_json()
    if 'long_url' not in data:
        return jsonify({'error': 'Please provide a long_url parameter'}), 400

    long_url = data['long_url']
    short_url = generate_short_url(long_url)
    url_repo.save_url_mapping(short_url, long_url)
    return jsonify({'short_url': f'/{short_url}'})

@app.route('/decrypt/<short_url>', methods=['GET'])
def decrypt(short_url):
    long_url = url_repo.get_long_url(short_url)
    if not long_url:
        return jsonify({'error': 'Short URL not found'}), 404

    return jsonify({'long_url': long_url})

if __name__ == '__main__':
    app.run(debug=True)