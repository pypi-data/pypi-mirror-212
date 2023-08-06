# TODOS LOS IMPORTS
# data manipulation and plotting


# from feature-engine
from feature_engine.imputation import AddMissingIndicator, MeanMedianImputer
from feature_engine.selection import DropFeatures

# the model
from sklearn.naive_bayes import GaussianNB

# from Scikit-learn
from sklearn.pipeline import Pipeline

from my_model.config.core import config

genero_pipe = Pipeline(
    [
        # ===== IMPUTATION =====
        (
            "drop_features",
            DropFeatures(features_to_drop=config.model_config.drop_features),
        ),
        # add missing indicator
        (
            "missing_indicator",
            AddMissingIndicator(variables=config.model_config.numerical_vars_with_na),
        ),
        # impute numerical variables with the mean
        (
            "mean_imputation",
            MeanMedianImputer(
                imputation_method="mean",
                variables=config.model_config.numerical_vars_with_na,
            ),
        ),
        ("GaussianNB", GaussianNB()),
    ]
)
