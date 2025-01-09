from typing import List

from pydantic import BaseModel, ConfigDict, conint, validator

OPERATORS = {
    "Aerolineas Argentinas",
    "Aeromexico",
    "Air Canada",
    "Air France",
    "Alitalia",
    "American Airlines",
    "Austral",
    "Avianca",
    "British Airways",
    "Copa Air",
    "Delta Air",
    "Gol Trans",
    "Grupo LATAM",
    "Iberia",
    "JetSmart SPA",
    "K.L.M.",
    "Lacsa",
    "Latin American Wings",
    "Oceanair Linhas Aereas",
    "Plus Ultra Lineas Aereas",
    "Qantas Airways",
    "Sky Airline",
    "United Airlines",
}


class Base(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Flight(Base):
    OPERA: str
    TIPOVUELO: str
    MES: conint(ge=1, le=12)

    @validator("OPERA")
    def check_valid_operator(cls, value):
        if value not in OPERATORS:
            raise ValueError(f"{value} is not a valid operator.")
        return value

    @validator("TIPOVUELO")
    def check_valid_flight_type(cls, value):
        if value not in ("N", "I"):
            raise ValueError(f"{value} is not a valid flight type.")
        return value


class PredictionRequest(Base):
    flights: List[Flight]


class PredictResponse(Base):
    predict: List[int]
