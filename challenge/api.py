from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .model import load_model
from .models import PredictionRequest, PredictResponse
from .preprocess import predict_request_to_features_df

# import joblib

app = FastAPI()
# model = joblib.load("model.joblib")
model = load_model("./data/data.csv")


@app.exception_handler(RequestValidationError)
async def custom_request_validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {"status": "OK"}


@app.post("/predict", status_code=200, response_model=PredictResponse)
async def post_predict(request: PredictionRequest) -> PredictResponse:
    features = predict_request_to_features_df(request.flights)

    res = model.predict(features)
    return PredictResponse(predict=res)
