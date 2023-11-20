class URLRepository:
    def __init__(self):
        self.url_store = {}

    def save_url_mapping(self, short_url, long_url):
        self.url_store[short_url] = long_url

    def get_long_url(self, short_url):
        return self.url_store.get(short_url)