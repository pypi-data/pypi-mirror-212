from typing import Dict, List, Optional

from paperqa.types import Answer
from pydantic import BaseModel, validator

# NOTE: Do not edit these - they come from the paperqa-sever


class UploadMetadata(BaseModel):
    filename: str
    citation: str
    key: Optional[str] = None


class Doc(BaseModel):
    key: str
    citation: str
    length: int
    doi: Optional[str] = None
    id: str


class DocsStatus(BaseModel):
    name: str
    llm: str
    summary_llm: str
    docs: List[Doc]
    doc_count: int
    writeable: bool = False


class QueryRequest(BaseModel):
    query: str
    llm: str = "gpt-4"
    summary_llm: str = "gpt-3.5-turbo"
    length: str = "as long as necessary"
    max_sources: int = 7
    consider_sources: int = 10

    @validator("max_sources")
    def max_sources_for_gpt(cls, v: int, values: dict, **kwargs) -> int:
        if "gpt" in values["llm"] and v > 8:
            raise ValueError("Max sources for GPT models is 8")
        return v


class AnswerResponse(BaseModel):
    answer: Answer
    usage: Dict[str, List[int]]
    bibtex: Dict[str, str]
