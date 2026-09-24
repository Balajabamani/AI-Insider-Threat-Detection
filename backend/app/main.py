from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import router

from app.services.activity_monitor import (
    start_monitoring
)


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(

    title="AI Insider Threat Detection",

    version="1.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=[

        "http://localhost:5173",

        "http://127.0.0.1:5173"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


# ============================================================
# ROUTES
# ============================================================

app.include_router(router)


# ============================================================
# START MONITORING WHEN SERVER STARTS
# ============================================================

@app.on_event("startup")
def startup_event():

    print()
    print(
        "Starting system-wide "
        "real-time monitoring..."
    )

    start_monitoring()


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return {

        "message":
            "AI Insider Threat Detection System Running",

        "monitoring":
            "System-wide real-time monitoring active"
    }