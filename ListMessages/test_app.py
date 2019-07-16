from app import app
from utils import redisdb
import pytest
import json
import xml.etree.ElementTree as ET

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.app_context():
        client = app.test_client()
        yield client

def test_resource_not_found(client):
    """Test API can not find resource."""
    response = client.get('/')
    data = json.loads(response.data)
    assert response.status_code == 404
    assert data['message']['error'] is not None

def test_undefined_version(client):
    """Test API support for undefined version."""
    response = client.get('/v3')
    data = json.loads(response.data)
    assert response.status_code == 400
    assert data['message']['error'] == 'Requested version not supported'

def test_v1_bad_request(client):
    """Test bad request for v1 with parameters"""
    response = client.get('/v1?format=XML')
    data = json.loads(response.data)
    assert response.status_code == 400
    assert data['message']['error'] == "This version does not accept additional parameters"

def test_v1_success(client):
    """Test version 1 success"""
    response = client.get('/v1')
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['messages'][0] is not None

def test_v1_url_field(client):
    """Test version 1 does not have url field"""
    response = client.get('/v1')
    data = json.loads(response.data)

    assert response.status_code == 200
    with pytest.raises(KeyError):
        assert data['messages'][0]['url'] is None

def test_v2_undefined_format(client):
    """Test API support for undefined format."""
    response = client.get('/v2?format=BYTE')
    data = json.loads(response.data)
    assert response.status_code == 400
    assert data['message']['error'] == 'Requested format not supported'

def test_v2_success_no_param(client):
    """Test version 2 success with no param"""
    response = client.get('/v2')
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['messages'][0]['url'] is not None

def test_v2_success_JSON(client):
    """Test version 2 success with no param"""
    response = client.get('/v2?format=JSON')
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['messages'][0]['url'] is not None

def test_v2_success_XML(client):
    """Test version 2 success with no param"""
    response = client.get('/v2?format=XML')
    root = ET.fromstring(response.data)

    assert response.status_code == 200
    assert root[0].tag == 'message'

@pytest.fixture(scope='session', autouse=True)
def mock_data():
    """Add mock data for testing"""
    success = redisdb.set("msg:test", "{\"title\":\"Test\",\"content\":\"API Testing\",\"sender\":\"Umar\",\"url\":\"www.umar.com\"}")
    yield success

    """Remove mock data for testing"""
    redisdb.delete("msg:test")