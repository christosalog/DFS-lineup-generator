
from src.Input.daily_lineups import get_daily_lineups
from src.Prediction.predict_pipeline import make_daily_predictions
from src.Modelling.lineup_opt import optimize_dk_lineup

if __name__ == "__main__":
    daily_lineups = get_daily_lineups()
    daily_predictions = make_daily_predictions(daily_lineups)
    optimized_lineup = optimize_dk_lineup(daily_predictions)
    print(optimized_lineup)


