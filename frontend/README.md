# Smart Water Waste Monitor — Dashboard

This folder contains the React dashboard for the Smart Water Waste Monitoring project.

## Run the dashboard

Open PowerShell in this `frontend` folder:

```powershell
cd C:\Users\LENOVO\Desktop\wm\frontend
npm install
npm run dev
```

Open the address printed by Vite, normally [http://localhost:5173](http://localhost:5173).

## Backend required

The dashboard reads data from the FastAPI backend. In a separate PowerShell window, start it first:

```powershell
cd C:\Users\LENOVO\Desktop\wm
.\.venv\Scripts\Activate.ps1
cd backend
uvicorn app.main:app --reload
```

Check that the backend is running at [http://127.0.0.1:8000/api/health](http://127.0.0.1:8000/api/health).

## Create demo data

With the backend still running, use a third PowerShell window:

```powershell
cd C:\Users\LENOVO\Desktop\wm
.\.venv\Scripts\Activate.ps1
python scripts\run_demo.py
```

Refresh the dashboard. The demo entry is clearly marked as mock/demo data because no trained custom waste model is included.

## Common issue

`npm run dev` only works inside this `frontend` folder because `package.json` is stored here. Do not run it from `C:\Users\LENOVO\Desktop\wm`.
