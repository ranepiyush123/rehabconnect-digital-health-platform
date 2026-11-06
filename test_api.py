import os
os.environ['DATABASE_URL']='sqlite://'
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from app import main

# Shared in-memory DB for test isolation from local demo data.
main.engine.dispose()
main.engine = main.create_engine('sqlite://',connect_args={'check_same_thread':False},poolclass=StaticPool)
main.SessionLocal=main.sessionmaker(main.engine)

def test_health():
    with TestClient(main.app) as client:
        assert client.get('/api/health').json()['status']=='ok'

def test_patient_and_summary():
    with TestClient(main.app) as client:
        assert len(client.get('/api/patients').json())==3
        assert client.get('/api/patients/1/summary').status_code==200
        assert client.get('/api/patients/999/summary').status_code==404

def test_checkin_validation_and_creation():
    with TestClient(main.app) as client:
        assert client.post('/api/checkins',json={'patient_id':1,'pain_score':11,'completed':True}).status_code==422
        result=client.post('/api/checkins',json={'patient_id':1,'pain_score':2,'completed':True,'notes':'Test'})
        assert result.status_code==201
        assert result.json()['pain_score']==2

def test_plan_creation():
    with TestClient(main.app) as client:
        response=client.post('/api/plans',json={'patient_id':2,'exercise':'Demo movement','frequency':'Daily','instructions':'Demo only'})
        assert response.status_code==201
        assert any(x['exercise']=='Demo movement' for x in client.get('/api/patients/2/plans').json())
