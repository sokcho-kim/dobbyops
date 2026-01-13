# API 비용 확인

유료 API 사용 현황을 확인하고 관리합니다.

## 비용 확인 명령

### 오늘 비용
```bash
python C:/Jimin/scrape-hub/shared/cost_tracker.py today
```

### 월간 비용
```bash
python C:/Jimin/scrape-hub/shared/cost_tracker.py month 2026-01
```

### 특정 날짜
```bash
python C:/Jimin/scrape-hub/shared/cost_tracker.py month YYYY-MM
```

## 비용 로깅 (API 사용 시)

### CLI로 수동 로깅
```bash
# Upstage Document Parse (페이지 기반)
python C:/Jimin/scrape-hub/shared/cost_tracker.py log upstage document_parse <project> --pages 72

# OpenAI (토큰 기반)
python C:/Jimin/scrape-hub/shared/cost_tracker.py log openai gpt-4o <project> --input 1000 --output 500

# 메모 추가
python C:/Jimin/scrape-hub/shared/cost_tracker.py log upstage document_parse khima --pages 30 --note "문제집 파싱"
```

### 코드에서 로깅
```python
from shared.cost_tracker import log_api_call

log_api_call(
    provider="upstage",
    api="document_parse",
    project="프로젝트명",
    pages=72,
    note="설명"
)
```

## 추적 대상 API

| Provider | API | 과금 단위 |
|----------|-----|----------|
| Upstage | document_parse | 페이지 |
| OpenAI | gpt-4o, gpt-4o-mini | 토큰 |
| OpenAI | text-embedding-3-* | 토큰 |
| Anthropic | claude-* | 토큰 |

## 데이터 위치

- 로그: `C:/Jimin/scrape-hub/data/tracking/api_costs.jsonl`
- 단가 설정: `C:/Jimin/scrape-hub/shared/config/api_pricing.yaml`

## 사용 예시

사용자가 `/cost-check`를 호출하면:
1. 오늘/이번 달 비용 요약 출력
2. Provider별, Project별 breakdown 제공
3. 이상 지출이 있으면 경고
