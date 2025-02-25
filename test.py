from fastapi import FastAPI,Depends,HTTPException,Header
from fastapi.security.api_key import APIKeyHeader
import joblib
from fastapi.middleware.cors import CORSMiddleware

API_KEY='Hello-World'
API_KEY_NAME='Authorization'
api_key_header=APIKeyHeader(name=API_KEY_NAME,auto_error=False)
app=FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:5000",
    "http://127.0.0.1:5000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


loaded_model = joblib.load('RandomForest.pkl')

@app.post('/predict')
async def predict(honeypot,mouse_movement,api_key):
    if api_key !='Hello-World':
        return {"Error" : "Envalid API Key"}
    
    else:
        honeypot = 1 if honeypot == "Yes" else 0 
        mouse_movement=1 if mouse_movement=='non linear' else 0
        prediction = loaded_model.predict([[honeypot, mouse_movement]]) 
        return {"prediction":prediction[0]}
    
    
# to run this api uvicorn test:app --reload
