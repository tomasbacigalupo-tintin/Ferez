"""Simple FastAPI server exposing WiFiFixCore functions."""

from fastapi import FastAPI
from pydantic import BaseModel

from .core import WiFiFixCore

app = FastAPI()
core = WiFiFixCore()


class FixResponse(BaseModel):
    success: bool


@app.post("/fix_all", response_model=FixResponse)
async def fix_all():
    success = core.fix_all()
    return {"success": success}


class DiagnoseResponse(BaseModel):
    connection: bool
    gateway: bool
    dhcp: bool
    ip_conflict: bool
    port_53: bool


@app.get("/diagnose", response_model=DiagnoseResponse)
async def diagnose():
    results = core.diagnose_network()
    return results
