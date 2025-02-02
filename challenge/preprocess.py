from datetime import datetime
from typing import List

import pandas as pd

from .models import Flight

FEATURES = [
    "OPERA_Latin American Wings",
    "MES_7",
    "MES_10",
    "OPERA_Grupo LATAM",
    "MES_12",
    "TIPOVUELO_I",
    "MES_4",
    "MES_11",
    "OPERA_Sky Airline",
    "OPERA_Copa Air",
]


def get_period_day(date: datetime):
    date_time = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").time()
    morning_min = datetime.strptime("05:00", "%H:%M").time()
    morning_max = datetime.strptime("11:59", "%H:%M").time()
    afternoon_min = datetime.strptime("12:00", "%H:%M").time()
    afternoon_max = datetime.strptime("18:59", "%H:%M").time()
    evening_min = datetime.strptime("19:00", "%H:%M").time()
    evening_max = datetime.strptime("23:59", "%H:%M").time()
    night_min = datetime.strptime("00:00", "%H:%M").time()
    night_max = datetime.strptime("4:59", "%H:%M").time()

    if date_time > morning_min and date_time < morning_max:
        return "mañana"
    elif date_time > afternoon_min and date_time < afternoon_max:
        return "tarde"
    elif (date_time > evening_min and date_time < evening_max) or (
        date_time > night_min and date_time < night_max
    ):
        return "noche"


def is_high_season(fecha: str):
    fecha_año = int(fecha.split("-")[0])
    fecha = datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S")
    range1_min = datetime.strptime("15-Dec", "%d-%b").replace(year=fecha_año)
    range1_max = datetime.strptime("31-Dec", "%d-%b").replace(year=fecha_año)
    range2_min = datetime.strptime("1-Jan", "%d-%b").replace(year=fecha_año)
    range2_max = datetime.strptime("3-Mar", "%d-%b").replace(year=fecha_año)
    range3_min = datetime.strptime("15-Jul", "%d-%b").replace(year=fecha_año)
    range3_max = datetime.strptime("31-Jul", "%d-%b").replace(year=fecha_año)
    range4_min = datetime.strptime("11-Sep", "%d-%b").replace(year=fecha_año)
    range4_max = datetime.strptime("30-Sep", "%d-%b").replace(year=fecha_año)

    if (
        (fecha >= range1_min and fecha <= range1_max)
        or (fecha >= range2_min and fecha <= range2_max)
        or (fecha >= range3_min and fecha <= range3_max)
        or (fecha >= range4_min and fecha <= range4_max)
    ):
        return 1
    else:
        return 0


def get_min_diff(data: pd.DataFrame) -> float:
    fecha_o = datetime.strptime(data["Fecha-O"], "%Y-%m-%d %H:%M:%S")
    fecha_i = datetime.strptime(data["Fecha-I"], "%Y-%m-%d %H:%M:%S")
    min_diff = ((fecha_o - fecha_i).total_seconds()) / 60
    return min_diff


def flight_to_feature(flight: Flight) -> dict:
    feature = {k: 0 for k in FEATURES}

    opera = f"OPERA_{flight.OPERA}"
    if opera in feature:
        feature[opera] = 1

    mes = f"MES_{flight.MES}"
    if mes in feature:
        feature[mes] = 1

    if flight.TIPOVUELO == "I":
        feature["TIPOVUELO_I"] = 1

    return feature


def predict_request_to_features_df(flights: List[Flight]) -> pd.DataFrame:
    features = pd.DataFrame([flight_to_feature(f) for f in flights])
    return features
