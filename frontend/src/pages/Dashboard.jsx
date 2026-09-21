import { useEffect, useState } from 'react'
import { api } from '../services/api'
import CameraFeed from '../components/CameraFeed'
import Statistics from '../components/Statistics'
import DetectionTable from '../components/DetectionTable'
import AlertPanel from '../components/AlertPanel'
import PollutionMap from '../components/PollutionMap'
export default function Dashboard() { const [detections,setDetections]=useState([]), [alerts,setAlerts]=useState([]), [statistics,setStatistics]=useState({}), [error,setError]=useState(''); useEffect(()=>{const load=async()=>{try {const [d,a,s]=await Promise.all([api.detections(),api.alerts(),api.statistics()]);setDetections(d);setAlerts(a);setStatistics(s);setError('')} catch(e){setError('Backend unavailable: start uvicorn app.main:app --reload from backend.') }};load();const id=setInterval(load,5000);return()=>clearInterval(id)},[]);return <main><header><div><h1>Smart Water Waste Monitoring</h1><p>YOLOv8 detection · GPS traceability · real-time alerts</p></div><span className="badge">{error ? 'Offline' : 'Monitoring'}</span></header>{error&&<div className="error">{error}</div>}<Statistics statistics={statistics} alerts={alerts.length}/><CameraFeed/><div className="grid"><div><AlertPanel alerts={alerts}/><DetectionTable detections={detections}/></div><PollutionMap detections={detections}/></div></main> }
