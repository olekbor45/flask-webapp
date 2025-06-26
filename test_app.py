import pytest #layout of the pytest taken from ChatGPT, testing conditions done by me
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

def test_exw(client):
    data = {
        'cargo_type': 'containerized',
        'transport_mode': 'road',
        'region': 'domestic',
        'role': 'seller',
        'responsibility_level': 'minimal',
        'insurance': 'no',
        'import_clearance': 'buyer',
        'delivery_point': 'origin_premises',
        'experience_level': 'expert',
    }
    response = client.post('/guide', data=data) #Source: ChatGPT
    assert b'EXW' in response.data 

def test_ddp(client):
    data = {
        'cargo_type': 'containerized',
        'transport_mode': 'road',
        'region': 'domestic',
        'role': 'seller',
        'responsibility_level': 'maximal',
        'insurance': 'yes',
        'import_clearance': 'seller',
        'delivery_point': 'destination_premises',
        'experience_level': 'expert',
    }
    response = client.post('/guide', data=data)
    assert b'DDP' in response.data

def test_fas(client):
    data = {
        'cargo_type': 'breakbulk',
        'transport_mode': 'sea',
        'region': 'international',
        'role': 'seller',
        'responsibility_level': 'shared',
        'insurance': 'no',
        'import_clearance': 'buyer',
        'delivery_point': 'port_of_shipment',
        'experience_level': 'intermediate',
    }
    response = client.post('/guide', data=data)
    assert b'FAS' in response.data

def test_dpu(client):
    data = {
        'cargo_type': 'project',
        'transport_mode': 'road',
        'region': 'international',
        'role': 'seller',
        'responsibility_level': 'maximal',
        'insurance': 'no',
        'import_clearance': 'buyer',
        'delivery_point': 'destination_premises',
        'experience_level': 'expert',
    }
    response = client.post('/guide', data=data)
    assert b'DPU' in response.data

def test_cif(client):
    data = {
        'cargo_type': 'containerized',
        'transport_mode': 'sea',
        'region': 'international',
        'role': 'seller',
        'responsibility_level': 'maximal',
        'insurance': 'yes',
        'import_clearance': 'buyer',
        'delivery_point': 'port_of_arrival',
        'experience_level': 'expert',
    }
    response = client.post('/guide', data=data)
    assert b'CIF' in response.data
