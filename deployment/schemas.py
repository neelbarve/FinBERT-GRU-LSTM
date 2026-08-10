from pydantic import BaseModel

class ArticleInput(BaseModel):
    article_title: str
    article_body: str
    future_return: float | None = None

class PipelineOutput(BaseModel):
    ranking: dict
    forecast_mse: float
    example_prediction: float | None
