from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uuid
import datetime

from agent.scanner import ShadowScanner
from agent.github_agent import GitHubAgent
import os
from dotenv import load_dotenv

from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()

app = FastAPI(title="ShadowCode API", description="DevSecOps AI Agent Backend")
github_agent = GitHubAgent()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for the demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

scanner = ShadowScanner()

# In-memory storage for demo purposes
scans = {}

class ScanRequest(BaseModel):
    target_path: str = os.getenv("TARGET_PATH", "./demo_files")

class ScanResult(BaseModel):
    id: str
    status: str
    vulnerabilities: List[dict]
    timestamp: str

@app.get("/")
async def root():
    return {"message": "ShadowCode AI Backend is running", "version": "1.0.0"}

@app.post("/scan", response_model=ScanResult)
async def trigger_scan(request: ScanRequest):
    scan_id = str(uuid.uuid4())
    
    # Perform actual scan using the ShadowScanner
    findings = scanner.scan_directory(request.target_path)
    
    scans[scan_id] = {
        "id": scan_id,
        "status": "completed",
        "vulnerabilities": findings,
        "timestamp": datetime.datetime.now().isoformat()
    }
    
    return scans[scan_id]

@app.get("/results", response_model=List[ScanResult])
async def get_all_results():
    return list(scans.values())

@app.get("/results/{scan_id}")
async def get_scan_result(scan_id: str):
    if scan_id not in scans:
        raise HTTPException(status_code=404, detail="Scan not found")
    return scans[scan_id]

@app.post("/remediate/{scan_id}")
async def remediate_scan(scan_id: str):
    if scan_id not in scans:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    scan_data = scans[scan_id]
    findings = scan_data["vulnerabilities"]
    
    if not findings:
        return {"message": "No vulnerabilities to fix"}
    
    result = github_agent.create_pr(findings)
    return result

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8001))
    uvicorn.run(app, host=host, port=port)
