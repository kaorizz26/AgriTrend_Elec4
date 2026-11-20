
from sktime.split import temporal_train_test_split

def prepare_train_test(commodity_data):
    """Split commodity prices and create six-month testing windows."""

    # Get the monthly price series
    monthly_prices = commodity_data["Price"]

    # Use the oldest 80% for training and newest 20% for testing
    train_data, test_data = temporal_train_test_split(
        monthly_prices, test_size=0.20
    )

    # Divide the testing period into complete six-month windows
    test_windows = []

    for start in range(0, len(test_data) - 5, 6):
        test_window = test_data.iloc[start:start + 6]
        test_windows.append(test_window)

    return monthly_prices, train_data, test_data, test_windows


import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error

def backtest_model(model, commodity_data, test_windows):
    """Evaluate a forecasting model using six-month testing windows."""

    backtest_results = []

    # Evaluate the model on each six-month window
    for test_window in test_windows:

        # Use only prices recorded before this testing window
        training_data = commodity_data[
            commodity_data.index < test_window.index[0]
        ]
        training_prices = training_data["Price"]

        # Create and train a fresh model
        current_model = model.clone()
        current_model.fit(training_prices)

        # Predict the next six months
        predicted_prices = current_model.predict(fh=range(1, 7))

        # Compare actual prices against predictions
        backtest_results.append({
            "Test Period": f"{test_window.index[0]} to {test_window.index[-1]}",
            "MAE": mean_absolute_error(test_window, predicted_prices),
            "RMSE": np.sqrt(mean_squared_error(test_window, predicted_prices))
        })

    return pd.DataFrame(backtest_results)



from src.forecasting import prepare_commodity_data, create_forecasting_models

def evaluate_commodity(data, category, commodity):
    """Evaluate and compare all three models for one commodity."""

    # Prepare the commodity's monthly price data
    commodity_data = prepare_commodity_data(data, category, commodity)

    # Create the chronological testing windows
    _, _, _, test_windows = prepare_train_test(commodity_data)

    evaluation_results = []

    # Evaluate each of the three approved models
    for model_name, model in create_forecasting_models().items():
        results = backtest_model(model, commodity_data, test_windows)

        evaluation_results.append({
            "Model": model_name,
            "MAE": results["MAE"].mean(),
            "RMSE": np.sqrt((results["RMSE"] ** 2).mean())
        })

    # Rank models by lowest MAE, then RMSE
    evaluation_df = pd.DataFrame(evaluation_results)

    return evaluation_df.sort_values(
        ["MAE", "RMSE"]
    ).reset_index(drop=True)


