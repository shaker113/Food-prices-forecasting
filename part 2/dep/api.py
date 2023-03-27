from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd

app = FastAPI()

class ScroingItem(BaseModel):
    category      :  int  
    commodity     :  int  
    month         :  int  
    year          :  int  
    is_ramdan     :  int  
    population    :  int  
    middle_east   :  int  
    world         :  int  
    jor_new_cases :  float
    jor_new_deaths:  float

with open('xgboost model.pkl', 'rb') as file:
    xgboost_model = pickle.load(file)

# @app.post('/')
# async def scroing_endpoint(item:ScroingItem):
#     # df = pd.DataFrame([item.dict().values()],columns=item.dict().keys())
#     input_list = [list(item.dict().values())]
#     # print(list(item.dict().values()))
#     predict_price = xgboost_model.predict(input_list)
#     return {"predict_price": float(predict_price)}
#     # return 1


@app.get('/')
async def scroing_endpoint(category      :  int,
    commodity     :  int,  
    month         :  int,  
    year          :  int,  
    is_ramdan     :  int,  
    population    :  int,  
    middle_east   :  int,  
    world         :  int,  
    jor_new_cases :  float,
    jor_new_deaths:  float):
    input_list = [[category,
                   commodity,
                   month,
                   year,
                   is_ramdan,
                   population,
                   middle_east,
                   world,
                   jor_new_cases,
                   jor_new_deaths]]
    predict_price = xgboost_model.predict(input_list)
    return {"predict_price": float(predict_price)}
    # return 1