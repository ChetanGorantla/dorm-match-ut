from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ Allow frontend requests from your deployed website (React Vite)
origins = [
    "http://localhost:5173",  # Local dev
    "https://your-frontend.com",  # Deployed frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "FastAPI is running!"}

@app.post("/ut-prediction")
async def predict(data: dict):
    # 🔹 Example processing logic (Replace with actual)
    top3 = ["Dorm A", "Dorm B", "Dorm C"]
    top10 = ["Dorm D", "Dorm E", "Dorm F"]
    
    return {"top3": top3, "top10": top10}
