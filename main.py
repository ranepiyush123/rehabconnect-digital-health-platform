"""RehabConnect prototype API. Synthetic data only; no authentication."""
from contextlib import asynccontextmanager
from datetime import date, datetime, timezone
from pathlib import Path
import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, ForeignKey, String, Integer, Date, DateTime, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session, sessionmaker

DB_URL = os.getenv('DATABASE_URL', 'sqlite:///./rehabconnect.db')
engine = create_engine(DB_URL, connect_args={'check_same_thread': False} if DB_URL.startswith('sqlite') else {})
SessionLocal = sessionmaker(engine)
class Base(DeclarativeBase): pass
class Patient(Base):
    __tablename__ = 'patients'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    condition: Mapped[str] = mapped_column(String(100))
    start_date: Mapped[date] = mapped_column(Date)
class Plan(Base):
    __tablename__ = 'plans'
    id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey('patients.id'))
    exercise: Mapped[str] = mapped_column(String(120))
    frequency: Mapped[str] = mapped_column(String(100))
    instructions: Mapped[str] = mapped_column(String(500))
class Checkin(Base):
    __tablename__ = 'checkins'
    id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey('patients.id'))
    pain_score: Mapped[int] = mapped_column(Integer)
    completed: Mapped[bool]
    notes: Mapped[str] = mapped_column(String(500), default='')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda:datetime.now(timezone.utc))

def seed():
    with SessionLocal() as db:
        if db.scalar(select(Patient.id).limit(1)) is not None: return
        db.add_all([
            Patient(id=1,name='Alex Morgan (fictional)',condition='Knee rehabilitation (demo)',start_date=date(2026,10,1)),
            Patient(id=2,name='Sam Taylor (fictional)',condition='Shoulder rehabilitation (demo)',start_date=date(2026,10,12)),
            Patient(id=3,name='Jordan Lee (fictional)',condition='Mobility rehabilitation (demo)',start_date=date(2026,10,20))])
        db.add_all([
            Plan(patient_id=1,exercise='Seated knee extension',frequency='2 sets daily',instructions='Follow clinician-provided instructions; demo only.'),
            Plan(patient_id=1,exercise='Supported heel raises',frequency='1 set daily',instructions='Follow clinician-provided instructions; demo only.'),
            Plan(patient_id=2,exercise='Gentle shoulder movement',frequency='1 set daily',instructions='Follow clinician-provided instructions; demo only.'),
            Plan(patient_id=3,exercise='Supported walking',frequency='As prescribed',instructions='Follow clinician-provided instructions; demo only.')])
        db.add_all([
            Checkin(patient_id=1,pain_score=5,completed=True,notes='Demo check-in'),
            Checkin(patient_id=1,pain_score=3,completed=True,notes='Demo check-in'),
            Checkin(patient_id=2,pain_score=4,completed=False,notes='Demo check-in')])
        db.commit()

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    seed()
    yield

app = FastAPI(title='RehabConnect API', version='0.1.0', lifespan=lifespan,
    description='Synthetic-data educational prototype. Not for clinical use.')
app.add_middleware(CORSMiddleware, allow_origins=['http://localhost:5173','http://127.0.0.1:5173'], allow_methods=['GET','POST'], allow_headers=['*'])

def get_db():
    with SessionLocal() as db: yield db

class CheckinCreate(BaseModel):
    patient_id: int = Field(gt=0)
    pain_score: int = Field(ge=0,le=10)
    completed: bool
    notes: str = Field(default='',max_length=500)
class PlanCreate(BaseModel):
    patient_id: int = Field(gt=0)
    exercise: str = Field(min_length=2,max_length=120)
    frequency: str = Field(min_length=2,max_length=100)
    instructions: str = Field(min_length=2,max_length=500)

def patient_or_404(db, patient_id):
    patient=db.get(Patient,patient_id)
    if patient is None: raise HTTPException(404,'Patient not found')
    return patient

def checkin_dict(c):
    return {'id':c.id,'patient_id':c.patient_id,'pain_score':c.pain_score,'completed':c.completed,'notes':c.notes,'created_at':c.created_at.isoformat()}

@app.get('/api/health')
def health(): return {'status':'ok','prototype':True}
@app.get('/api/patients')
def patients(db:Session=Depends(get_db)):
    return [{'id':p.id,'name':p.name,'condition':p.condition,'start_date':p.start_date.isoformat()} for p in db.scalars(select(Patient).order_by(Patient.id))]
@app.get('/api/patients/{patient_id}')
def patient_detail(patient_id:int,db:Session=Depends(get_db)):
    p=patient_or_404(db,patient_id)
    return {'id':p.id,'name':p.name,'condition':p.condition,'start_date':p.start_date.isoformat()}
@app.get('/api/patients/{patient_id}/plans')
def plans(patient_id:int,db:Session=Depends(get_db)):
    patient_or_404(db,patient_id)
    return [{'id':p.id,'exercise':p.exercise,'frequency':p.frequency,'instructions':p.instructions} for p in db.scalars(select(Plan).where(Plan.patient_id==patient_id).order_by(Plan.id))]
@app.post('/api/plans',status_code=201)
def add_plan(data:PlanCreate,db:Session=Depends(get_db)):
    patient_or_404(db,data.patient_id)
    p=Plan(**data.model_dump());db.add(p);db.commit();db.refresh(p)
    return {'id':p.id,'patient_id':p.patient_id,'exercise':p.exercise,'frequency':p.frequency,'instructions':p.instructions}
@app.get('/api/patients/{patient_id}/checkins')
def checkins(patient_id:int,db:Session=Depends(get_db)):
    patient_or_404(db,patient_id)
    return [checkin_dict(c) for c in db.scalars(select(Checkin).where(Checkin.patient_id==patient_id).order_by(Checkin.id))]
@app.post('/api/checkins',status_code=201)
def add_checkin(data:CheckinCreate,db:Session=Depends(get_db)):
    patient_or_404(db,data.patient_id)
    c=Checkin(**data.model_dump());db.add(c);db.commit();db.refresh(c)
    return checkin_dict(c)
@app.get('/api/patients/{patient_id}/summary')
def summary(patient_id:int,db:Session=Depends(get_db)):
    patient_or_404(db,patient_id)
    cs=list(db.scalars(select(Checkin).where(Checkin.patient_id==patient_id).order_by(Checkin.id)))
    return {'total_checkins':len(cs),'completed_sessions':sum(c.completed for c in cs),
        'completion_rate':round(sum(c.completed for c in cs)/len(cs)*100,1) if cs else 0,
        'latest_pain_score':cs[-1].pain_score if cs else None,
        'pain_history':[{'date':c.created_at.date().isoformat(),'score':c.pain_score,'id':c.id} for c in cs]}
