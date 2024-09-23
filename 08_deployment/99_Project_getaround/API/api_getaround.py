import os
import pickle
import joblib
import uvicorn
import pandas as pd

from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

app = FastAPI()

with open("./assets/full_pipeline.pkl", "rb") as file:
    preprocessor = pickle.load(file)

model = joblib.load("./assets/model_xgb.pkl")


class InputData(BaseModel):
    input: list


# -----------------------------------------------------------------------------
# TODO : test if we can use default parameters and get rid of "string"
# @app.get("/items/")
# def read_items(
#     q: str = "default_value",
#     limit: int = 10):

#     return {
#         "q": q,
#         "limit": limit
#     }


# -----------------------------------------------------------------------------
@app.post("/predict")
async def predict(data: InputData):
    try:
        input_data = data.input
        input_features = [
            "model_key",
            "mileage",
            "engine_power",
            "fuel",
            "paint_color",
            "car_type",
            "private_parking_available",
            "has_gps",
            "has_air_conditioning",
            "automatic_car",
            "has_getaround_connect",
            "has_speed_regulator",
            "winter_tires",
        ]
        input_df = pd.DataFrame(input_data, columns=input_features)
        preprocessed_data = preprocessor.transform(input_df)
        prediction = model.predict(preprocessed_data)
        return {"prediction": f"{prediction[0]:.2f} €"}
    except Exception as e:
        print(str(e))
        raise HTTPException(
            status_code=500,
            detail="Error api-getaround. Check that the number of parameters and their spelling are correct.",
        )


# -----------------------------------------------------------------------------
@app.get("/docs")
async def get_docs():
    return {"docs_url": "/docs"}


# -----------------------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def read_root():
    html_content = """
        <html>
            <head>
                <title>API getaround</title>
            </head>
            <body>
                <h1>Welcome to the getaround API</h1>
                    <ul>
                        <li>Use the endpoint <code>/predict</code> to make predictions</li>
                        <li>Use the endpoint <code>/docs</code> to test the API<br />
                            <ul>
                                <li>Copy and paste the line below for your first test: <code>["Citro&euml;n", "140411", "100", "diesel", "black", "convertible", true, true, false, false, true, true, true]</code></li>
                                <li><code></code>In plain English, the features are : <code>model_key, mileage, engine_power, fuel, paint_color, car_type, private_parking_available, has_gps, has_air_conditioning, automatic_car, has_getaround_connect, has_speed_regulator, winter_tires</code></li>
                                <li>If you run into problems, start by checking that there are 2 square brackets around the parameter list, that you've written <strong>true</strong> and <strong>false</strong> (and not True and False) and that the model is spelled correctly</li>
                            </ul>
                        </li>
                    </ul>
                    <p>To use the API from a terminal, try a request similar to : <code>curl -i -H "Content-Type: application/json" -X POST -d '{"input": [["Citro&euml;n", "140411", "100", "diesel", "black", "convertible", true, true, false, false, true, true, true]]}' <a href="https://api-getaround-4ece015745ea.herokuapp.com/predict">https://api-getaround-4ece015745ea.herokuapp.com/predict </a></code></p>
                    <p>&nbsp;</p>
            </body>
        </html>
    """
    return html_content


# -----------------------------------------------------------------------------
if __name__ == "__main__":
    # either set ``port`` to the value of the environment variable PORT or use 8000
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
