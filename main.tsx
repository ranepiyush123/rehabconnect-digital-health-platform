import React, {useEffect,useState} from 'react';
import {createRoot} from 'react-dom/client';
import {LineChart,Line,CartesianGrid,XAxis,YAxis,Tooltip,ResponsiveContainer} from 'recharts';
import {Activity,HeartPulse,Users,ClipboardList,ShieldAlert} from 'lucide-react';
import './style.css';
type Patient={id:number;name:string;condition:string;start_date:string};
type Plan={id:number;exercise:string;frequency:string;instructions:string};
type Checkin={id:number;pain_score:number;completed:boolean;notes:string;created_at:string};
type Summary={total_checkins:number;completed_sessions:number;completion_rate:number;latest_pain_score:number|null;pain_history:{id:number;date:string;score:number}[]};
async function api<T>(path:string,options?:RequestInit):Promise<T>{const r=await fetch('/api'+path,{...options,headers:{'Content-Type':'application/json',...options?.headers}});if(!r.ok)throw new Error((await r.text()).slice(0,180));return r.json();}
function App(){
 const [role,setRole]=useState<'clinician'|'patient'>('clinician');
 const [patients,setPatients]=useState<Patient[]>([]);const [selected,setSelected]=useState(1);
 const [plans,setPlans]=useState<Plan[]>([]);const [checkins,setCheckins]=useState<Checkin[]>([]);
 const [summary,setSummary]=useState<Summary|null>(null);const [pain,setPain]=useState(3);
 const [completed,setCompleted]=useState(true);const [notes,setNotes]=useState('');
 const [exercise,setExercise]=useState('');const [frequency,setFrequency]=useState('Daily');
 const [instructions,setInstructions]=useState('Demo exercise instructions only');
 const [message,setMessage]=useState('');const [busy,setBusy]=useState(false);
 const patient=patients.find(p=>p.id===selected);
 async function refresh(id:number){try{const [p,c,s]=await Promise.all([api<Plan[]>(`/patients/${id}/plans`),api<Checkin[]>(`/patients/${id}/checkins`),api<Summary>(`/patients/${id}/summary`)]);setPlans(p);setCheckins(c);setSummary(s);}catch(e){setMessage(String(e));}}
 useEffect(()=>{api<Patient[]>('/patients').then(setPatients).catch(e=>setMessage(String(e)));},[]);
 useEffect(()=>{void refresh(selected);},[selected]);
 async function saveCheckin(e:React.FormEvent){e.preventDefault();setBusy(true);try{await api('/checkins',{method:'POST',body:JSON.stringify({patient_id:selected,pain_score:pain,completed,notes})});setNotes('');setMessage('Check-in saved');await refresh(selected);}catch(e){setMessage(String(e));}finally{setBusy(false);}}
 async function savePlan(e:React.FormEvent){e.preventDefault();setBusy(true);try{await api('/plans',{method:'POST',body:JSON.stringify({patient_id:selected,exercise,frequency,instructions})});setExercise('');setMessage('Plan added');await refresh(selected);}catch(e){setMessage(String(e));}finally{setBusy(false);}}
 return <div className="layout"><aside><div className="brand"><HeartPulse size={26}/> RehabConnect</div><div className="side-note">DIGITAL HEALTH PROTOTYPE</div><button className={role==='clinician'?'nav active':'nav'} onClick={()=>setRole('clinician')}><Users size={18}/> Clinician view</button><button className={role==='patient'?'nav active':'nav'} onClick={()=>setRole('patient')}><Activity size={18}/> Patient view</button><div className="aside-bottom">Synthetic patient records<br/>Not for clinical use</div></aside>
 <main><header><div><div className="eyebrow">REHABILITATION MANAGEMENT</div><h1>{role==='clinician'?'Clinician overview':'My rehabilitation journey'}</h1><p className="muted">Track rehabilitation plans and patient-reported outcomes.</p></div><div className="pill">● Demonstration environment</div></header>
 <div className="notice"><ShieldAlert size={18}/> <span>Educational prototype only. No login, clinical validation, or real patient data. The role switch is a UI demo, not access control.</span></div>
 <div className="selector"><label htmlFor="patient">{role==='clinician'?'Select fictional patient':'Demo patient'}</label><select id="patient" value={selected} onChange={e=>setSelected(Number(e.target.value))}>{patients.map(p=><option key={p.id} value={p.id}>{p.name}</option>)}</select><span className="muted">{patient?.condition}</span></div>
 {message&&<div role="status" className="feedback">{message}<button onClick={()=>setMessage('')}>Dismiss</button></div>}
 <div className="stats"><div className="stat"><span>Check-ins</span><strong>{summary?.total_checkins??'—'}</strong><small>Patient reports</small></div><div className="stat"><span>Exercise completion</span><strong>{summary?.completion_rate??0}%</strong><small>Reported sessions</small></div><div className="stat"><span>Latest pain score</span><strong>{summary?.latest_pain_score??'—'}<small> / 10</small></strong><small>Self-reported, not diagnostic</small></div></div>
 <div className="columns"><section className="panel"><div className="panel-title"><h2><Activity size={20}/> Pain score trend</h2><span className="muted">Patient reported</span></div>{summary?.pain_history.length?<div className="chart"><ResponsiveContainer width="100%" height="100%"><LineChart data={summary.pain_history.map((x,i)=>({...x,visit:`#${i+1}`}))}><CartesianGrid strokeDasharray="3 3" stroke="#e8eef3"/><XAxis dataKey="visit"/><YAxis domain={[0,10]}/><Tooltip/><Line type="monotone" dataKey="score" stroke="#168b88" strokeWidth={3} dot={{r:4}}/></LineChart></ResponsiveContainer></div>:<p>No check-ins yet.</p>}</section>
 <section className="panel"><div className="panel-title"><h2><ClipboardList size={20}/> Rehabilitation plan</h2></div>{plans.map(p=><div className="plan" key={p.id}><b>{p.exercise}</b><span className="tag">{p.frequency}</span><p>{p.instructions}</p></div>)}{role==='clinician'&&<form onSubmit={savePlan} className="form"><h3>Add a demo exercise</h3><label>Exercise name<input required minLength={2} value={exercise} onChange={e=>setExercise(e.target.value)} placeholder="e.g. Demo movement"/></label><label>Frequency<input required minLength={2} value={frequency} onChange={e=>setFrequency(e.target.value)}/></label><label>Instructions<input required minLength={2} value={instructions} onChange={e=>setInstructions(e.target.value)}/></label><button disabled={busy}>Add exercise</button></form>}</section></div>
 <div className="columns"><section className="panel"><h2>Submit patient check-in</h2><form className="form" onSubmit={saveCheckin}><label>Pain score: <strong>{pain}/10</strong><input type="range" min="0" max="10" value={pain} onChange={e=>setPain(Number(e.target.value))}/></label><label className="check"><input type="checkbox" checked={completed} onChange={e=>setCompleted(e.target.checked)}/> Exercises completed</label><label>Notes<textarea maxLength={500} value={notes} onChange={e=>setNotes(e.target.value)} placeholder="How did the session go?"/></label><button disabled={busy}>Save check-in</button></form></section>
 <section className="panel"><h2>Recent check-ins</h2><div className="table-wrap"><table><thead><tr><th>Date</th><th>Pain</th><th>Completed</th></tr></thead><tbody>{[...checkins].reverse().map(c=><tr key={c.id}><td>{new Date(c.created_at).toLocaleDateString()}</td><td>{c.pain_score}/10</td><td>{c.completed?'Yes':'No'}</td></tr>)}</tbody></table></div></section></div>
 <footer>RehabConnect is a fictional, non-clinical software portfolio project. No treatment guidance or clinical decision support is provided.</footer></main></div>;
}
createRoot(document.getElementById('root')!).render(<React.StrictMode><App/></React.StrictMode>);
