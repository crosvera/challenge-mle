from typing import List, Tuple, Union

import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split

from .preprocess import FEATURES, get_min_diff, get_period_day, is_high_season


class DelayModel:

    def __init__(self):
        self.features_columns = FEATURES
        scale = 4.4402380952380955
        self._model = xgb.XGBClassifier(
            random_state=1, learning_rate=0.01, scale_pos_weight=scale
        )

    def preprocess(
        self, data: pd.DataFrame, target_column: str = None
    ) -> Union[Tuple[pd.DataFrame, pd.DataFrame], pd.DataFrame]:
        """
        Prepare raw data for training or predict.

        Args:
            data (pd.DataFrame): raw data.
            target_column (str, optional): if set, the target is returned.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: features and target.
            or
            pd.DataFrame: features.
        """

        data["period_day"] = data["Fecha-I"].apply(get_period_day)
        data["high_season"] = data["Fecha-I"].apply(is_high_season)
        data["min_diff"] = data.apply(get_min_diff, axis=1)

        threshold_in_minutes = 15
        data["delay"] = np.where(data["min_diff"] > threshold_in_minutes, 1, 0)

        features = pd.concat(
            [
                pd.get_dummies(data["OPERA"], prefix="OPERA"),
                pd.get_dummies(data["TIPOVUELO"], prefix="TIPOVUELO"),
                pd.get_dummies(data["MES"], prefix="MES"),
            ],
            axis=1,
        )
        # target = data['delay']
        if target_column is None:
            self.fit(features[self.features_columns], data[["delay"]])
            return features[self.features_columns]

        return features[self.features_columns], data[[target_column]]

    def fit(self, features: pd.DataFrame, target: pd.DataFrame) -> None:
        """
        Fit model with preprocessed data.

        Args:
            features (pd.DataFrame): preprocessed data.
            target (pd.DataFrame): target.
        """
        x_train2, x_test2, y_train2, y_test2 = train_test_split(
            features, target, test_size=0.33, random_state=42
        )
        self._model.fit(x_train2, y_train2)
        return

    def predict(self, features: pd.DataFrame) -> List[int]:
        """
        Predict delays for new flights.

        Args:
            features (pd.DataFrame): preprocessed data.

        Returns:
            (List[int]): predicted targets.
        """
        return list(int(i) for i in self._model.predict(features))


def load_model(csvfile: str) -> DelayModel:
    model = DelayModel()
    csv = pd.read_csv(csvfile)

    features, target = model.preprocess(data=csv, target_column="delay")
    model.fit(features, target)

    return model
