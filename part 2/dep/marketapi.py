from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd

app2 = FastAPI()

class ScroingItem(BaseModel):
    commodity  : int  
    month      : int  
    year       : int  
    price_x    : float
    market     : int  

with open('market model.pkl', 'rb') as file:
    market_model = pickle.load(file)

@app2.post('/')
async def scroing_endpoint(item:ScroingItem):
    df = pd.DataFrame([item.dict().values()],columns=item.dict().keys())
    predict_price = market_model.predict(df)
    return {"predict_price": float(predict_price)}