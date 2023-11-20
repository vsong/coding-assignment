from repositories.url_repository import URLRepository

import pytest

@pytest.fixture
def url_repository():
    return URLRepository()

def test_save_and_retrieve_url(url_repository):
    short_url = "abc123"
    long_url = "https://google.com"
    url_repository.save_url_mapping(short_url, long_url)
    retrieved_url = url_repository.get_long_url(short_url)
    assert retrieved_url == long_url

def test_get_nonexistent_url(url_repository):
    short_url = "nonexistent"
    retrieved_url = url_repository.get_long_url(short_url)
    assert retrieved_url is None
