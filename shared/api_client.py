# -*- coding: utf-8 -*-
"""
API 클라이언트 래퍼
- Upstage, OpenAI 호출 시 자동 비용 로깅
"""
import os
import json
import requests
from pathlib import Path
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

from .cost_tracker import log_api_call

# 환경변수 로드
load_dotenv()


class UpstageClient:
    """Upstage API 클라이언트"""

    BASE_URL = "https://api.upstage.ai/v1/document-ai"

    def __init__(self, api_key: Optional[str] = None, project: str = "default"):
        self.api_key = api_key or os.getenv("UPSTAGE_API_KEY")
        self.project = project

        if not self.api_key:
            raise ValueError("UPSTAGE_API_KEY not found")

    def document_parse(
        self,
        file_path: str,
        output_format: str = "html",
        note: str = ""
    ) -> Dict[str, Any]:
        """Document Parse API 호출"""

        url = f"{self.BASE_URL}/document-parse"
        headers = {"Authorization": f"Bearer {self.api_key}"}

        with open(file_path, 'rb') as f:
            files = {"document": f}
            data = {"output_formats": f'["{output_format}"]'}
            response = requests.post(url, headers=headers, files=files, data=data)

        result = response.json()

        # 페이지 수 추출 (응답에서)
        pages = result.get('usage', {}).get('pages', 1)

        # 비용 로깅
        log_api_call(
            provider="upstage",
            api="document_parse",
            project=self.project,
            pages=pages,
            note=note or f"file: {Path(file_path).name}"
        )

        return result

    def ocr(
        self,
        file_path: str,
        note: str = ""
    ) -> Dict[str, Any]:
        """OCR API 호출"""

        url = f"{self.BASE_URL}/ocr"
        headers = {"Authorization": f"Bearer {self.api_key}"}

        with open(file_path, 'rb') as f:
            files = {"document": f}
            response = requests.post(url, headers=headers, files=files)

        result = response.json()
        pages = result.get('usage', {}).get('pages', 1)

        log_api_call(
            provider="upstage",
            api="ocr",
            project=self.project,
            pages=pages,
            note=note or f"file: {Path(file_path).name}"
        )

        return result


class OpenAIClient:
    """OpenAI API 클라이언트"""

    BASE_URL = "https://api.openai.com/v1"

    def __init__(self, api_key: Optional[str] = None, project: str = "default"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.project = project

        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found")

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-4o-mini",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        note: str = ""
    ) -> Dict[str, Any]:
        """Chat Completion API 호출"""

        url = f"{self.BASE_URL}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature
        }
        if max_tokens:
            payload["max_tokens"] = max_tokens

        response = requests.post(url, headers=headers, json=payload)
        result = response.json()

        # 토큰 사용량 추출
        usage = result.get('usage', {})
        input_tokens = usage.get('prompt_tokens', 0)
        output_tokens = usage.get('completion_tokens', 0)

        # 비용 로깅
        log_api_call(
            provider="openai",
            api=model,
            project=self.project,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            note=note
        )

        return result

    def embedding(
        self,
        texts: List[str],
        model: str = "text-embedding-3-small",
        note: str = ""
    ) -> Dict[str, Any]:
        """Embedding API 호출"""

        url = f"{self.BASE_URL}/embeddings"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": model,
            "input": texts
        }

        response = requests.post(url, headers=headers, json=payload)
        result = response.json()

        usage = result.get('usage', {})
        input_tokens = usage.get('total_tokens', 0)

        log_api_call(
            provider="openai",
            api=model,
            project=self.project,
            input_tokens=input_tokens,
            note=note
        )

        return result


# 편의 함수
def get_upstage_client(project: str = "default") -> UpstageClient:
    """Upstage 클라이언트 생성"""
    return UpstageClient(project=project)


def get_openai_client(project: str = "default") -> OpenAIClient:
    """OpenAI 클라이언트 생성"""
    return OpenAIClient(project=project)
