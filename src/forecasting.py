
import pandas as pd

def prepare_commodity_data(data, category, commodity):
    """Prepare one commodity's monthly price records for forecasting."""

    # Select the requested category and commodity
    commodity_data = data[
        (data["Category"] == category) &
        (data["Commodity"] == commodity)
    ].copy()

    # Arrange the records from oldest to newest
    commodity_data = commodity_data.sort_values("Date")

    # Use monthly dates as the time-series index
    commodity_data = commodity_data.set_index("Date").asfreq("MS")

    # Convert monthly timestamps into monthly periods
    commodity_data.index = commodity_data.index.to_period("M")

    return commodity_data


from sktime.forecasting.naive import NaiveForecaster
from sktime.forecasting.exp_smoothing import ExponentialSmoothing
from sktime.forecasting.arima import AutoARIMA

def create_forecasting_models():
    """Create the three approved forecasting models."""

    models = {
        # Baseline: use prices from the same season last year
        "Seasonal Naive": NaiveForecaster(
            strategy="last", sp=12
        ),
        
        # Capture trends and yearly seasonal patterns
        "Holt-Winters": ExponentialSmoothing(
            trend="add", seasonal="add", sp=12
        ),
        
        # Automatically select ARIMA parameters
        "AutoARIMA": AutoARIMA(
            seasonal=False,
            stepwise=True,
            suppress_warnings=True
        )
    }

    return models


def fit_and_forecast(model, monthly_prices, forecast_months=6):
    """Train a model on historical prices and forecast future months."""

    # Create a fresh copy of the selected model
    fitted_model = model.clone()

    # Train using all available historical prices
    fitted_model.fit(monthly_prices)

    # Predict the specified number of future months
    predicted_prices = fitted_model.predict(
        fh=range(1, forecast_months + 1)
    )

    return fitted_model, predicted_prices




# Generate six-month forecasts for a selected commodity
def forecast_commodity(data, category, commodity, best_models_df):
    """Train the best model and return its forecasts and fitted model."""

    # Prepare the commodity's historical monthly prices
    commodity_data = prepare_commodity_data(data, category, commodity)
    monthly_prices = commodity_data["Price"]

    # Find the selected model and its evaluation metrics
    selected_result = best_models_df[
        (best_models_df["Category"] == category) &
        (best_models_df["Commodity"] == commodity)
    ].iloc[0]

    model_name = selected_result["Model"]

    # Create and train the selected model using all historical prices
    model = create_forecasting_models()[model_name]
    fitted_model, predicted_prices = fit_and_forecast(
        model, monthly_prices, forecast_months=6
    )

    # Organize forecasts with historical evaluation metrics
    forecast_results = pd.DataFrame({
        "Category": category,
        "Commodity": commodity,
        "Last Observed Date": str(monthly_prices.index[-1]),
        "Last Observed Price": monthly_prices.iloc[-1],
        "Forecast Date": predicted_prices.index.astype(str),
        "Forecast Price": predicted_prices.to_numpy(),
        "Model": model_name,
        "MAE": selected_result["MAE"],
        "RMSE": selected_result["RMSE"]
    })

    return forecast_results, fitted_model
