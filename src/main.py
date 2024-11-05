# src/main.py

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes.broker_routes import router as broker_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Investment Simulation API",
    description="An API for processing investment simulation data.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)
app.include_router(broker_router)

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
