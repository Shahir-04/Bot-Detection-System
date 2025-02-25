# from fastapi import FastAPI, Request
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from scipy.stats import linregress
# import joblib

# # Load the pre-trained model
# loaded_model = joblib.load('RandomForest.pkl')

# app = FastAPI()

# # Configure CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Update with specific origins in production
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# class PredictionRequest(BaseModel):
#     mouse_movements: list
#     hidden_name: str


# @app.get("/test")
# def testapp():
#     return "Test"

# @app.post("/predict")
# async def predict(request: PredictionRequest):
#     hidden_name = 1 if request.hidden_name else 0

#     x = [movement['x'] for movement in request.mouse_movements]
#     y = [movement['y'] for movement in request.mouse_movements]

#     if len(x) < 2 or len(y) < 2:
#         return {"error": "Insufficient mouse movement data for analysis."}

#     slope, intercept, r_value, p_value, std_err = linregress(x, y)

#     mouse_movement = 1 if r_value**2 <= 0.95 else 0

#     prediction = loaded_model.predict([[hidden_name, mouse_movement]])
#     return {"user": prediction[0]}

from fastapi import FastAPI,Depends,HTTPException,Header
from fastapi.security.api_key import APIKeyHeader
import joblib
from scipy.stats import linregress
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

# def verify_api_key(x_api_key:str=Depends(api_key_header)):
#     if x_api_key ==API_KEY:
#         return api_key_header
#     else:
#         raise HTTPException(status_code=403,detail="Invalid API_KEY")
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