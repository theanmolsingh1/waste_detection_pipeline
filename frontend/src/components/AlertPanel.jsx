import DetectionCard from './DetectionCard'
export default function AlertPanel({ alerts }) { return <section className="panel"><h2>Recent alerts</h2>{alerts.length ? alerts.slice(0,3).map(d => <DetectionCard key={d.id} detection={d}/>) : <p>No alerts yet.</p>}</section> }
