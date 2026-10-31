from pydantic import BaseModel, Field

class GridLoadInput(BaseModel):
    temperature_celsius: float = Field(..., ge=-30.0, le=50.0, description="Ambient temperature in °C")
    hour_of_day: int = Field(..., ge=0, le=23, description="Hour of the day (0-23)")
    day_of_week: int = Field(..., ge=0, le=6, description="Day of week (0=Mon, 6=Sun)")
    is_holiday: int = Field(..., ge=0, le=1, description="Binary flag for bank holidays")

class GridLoadPrediction(BaseModel):
    predicted_load_mw: float
    model_version: str