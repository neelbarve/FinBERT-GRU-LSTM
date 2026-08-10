from fastapi import APIRouter
from deployment.schemas import ArticleInput, PipelineOutput
from deployment.service import run_pipeline_service

router = APIRouter(prefix="/pipeline", tags=["pipeline"])

@router.post("/run", response_model=PipelineOutput)
def run_pipeline(article_batch: list[ArticleInput]):
    return run_pipeline_service(article_batch)
