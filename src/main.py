from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# ✅ Allow frontend requests from React (Vite) and deployed frontend
origins = [
    "http://localhost:5173",  # Local React development
    "https://your-deployed-frontend.com"  # Deployed React app
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # ✅ Allows your frontend
    allow_credentials=True,
    allow_methods=["*"],  # ✅ Allows GET, POST, etc.
    allow_headers=["*"],  # ✅ Allows Content-Type, Authorization, etc.
)

# ✅ Define expected input format using Pydantic
class PredictionRequest(BaseModel):
    occupants: int
    bathroom: str
    budget: int
    accommodation: str

@app.get("/")
async def root():
    return {"message": "FastAPI is running!"}

@app.post("/ut-prediction")
async def predict(data: PredictionRequest):
    """ Mock function to return dorm predictions. """
    if data.occupants < 1:
        raise HTTPException(status_code=400, detail="Invalid number of occupants.")

    return {
        "top3": ["Dorm A", "Dorm B", "Dorm C"],
        "top10": ["Dorm D", "Dorm E", "Dorm F"]
    }

# ✅ Run FastAPI locally with:
# uvicorn main:app --host 0.0.0.0 --port 8000 --reload
