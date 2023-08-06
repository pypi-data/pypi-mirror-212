import json
from typing import Any, BinaryIO, Dict, List, Union

import requests

from .auth import get_pqa_key
from .models import AnswerResponse, DocsStatus, QueryRequest, UploadMetadata


def upload_files(
    bibliography: str,
    files: List[BinaryIO],
    metadatas: List[UploadMetadata],
    public: bool = False,
) -> List[Dict[str, Any]]:
    if len(files) != len(metadatas):
        raise ValueError("Number of files and metadata must match")

    if public:
        if not bibliography.startswith("public:"):
            bibliography = f"public:{bibliography}"
    url = f"https://paperqa.app/api/docs/{bibliography}/upload"

    files_data = [(("files", (file))) for file in files]
    with requests.Session() as session:
        response = session.post(
            url,
            files=files_data,
            data=dict(metadata=json.dumps([metadata.dict() for metadata in metadatas])),
            headers={"Authorization": f"Bearer {get_pqa_key()}"},
        )
        response.raise_for_status()
        result: List[Dict[str, Any]] = response.json()
        return result


def delete_bibliography(bibliography: str, public: bool = False) -> None:
    if public:
        if not bibliography.startswith("public:"):
            bibliography = f"public:{bibliography}"
    url = f"https://paperqa.app/db/docs/delete/{bibliography}"
    with requests.Session() as session:
        response = session.get(
            url,
            headers={"Authorization": f"Bearer {get_pqa_key()}"},
        )
        response.raise_for_status()


def get_bibliography(bibliography: str, public: bool = False) -> DocsStatus:
    if public:
        if not bibliography.startswith("public:"):
            bibliography = f"public:{bibliography}"
    url = f"https://paperqa.app/api/docs/status/{bibliography}"
    with requests.Session() as session:
        response = session.get(
            url,
            headers={"Authorization": f"Bearer {get_pqa_key()}"},
        )
        response.raise_for_status()
        result = DocsStatus(**response.json())
        return result


def agent_query(bibliography: str, query: Union[QueryRequest, str]) -> AnswerResponse:
    if isinstance(query, str):
        query = QueryRequest(query=query)
    url = f"https://paperqa.app/api/agent/{bibliography}"
    with requests.Session() as session:
        response = session.post(
            url, json=query.dict(), headers={"Authorization": f"Bearer {get_pqa_key()}"}
        )
        response.raise_for_status()
        result = AnswerResponse(**response.json())
        return result
