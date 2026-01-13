# -*- coding: utf-8 -*-
"""
API 비용 추적 모듈
- API 호출 로깅
- 일/주/월별 집계
"""
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any
import yaml

# 경로 설정
BASE_DIR = Path(__file__).parent.parent
TRACKING_DIR = BASE_DIR / 'data' / 'tracking'
COST_LOG_PATH = TRACKING_DIR / 'api_costs.jsonl'
PRICING_PATH = BASE_DIR / 'shared' / 'config' / 'api_pricing.yaml'

# 폴더 생성
TRACKING_DIR.mkdir(parents=True, exist_ok=True)


def load_pricing() -> Dict:
    """API 단가 설정 로드"""
    if PRICING_PATH.exists():
        with open(PRICING_PATH, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    return {}


def calculate_cost(
    provider: str,
    api: str,
    input_tokens: int = 0,
    output_tokens: int = 0,
    pages: int = 0
) -> float:
    """비용 계산"""
    pricing = load_pricing()

    if provider not in pricing:
        return 0.0

    provider_pricing = pricing[provider]

    # 페이지 기반 (Upstage)
    if api in provider_pricing and 'unit' in provider_pricing[api]:
        if provider_pricing[api]['unit'] == 'page':
            return pages * provider_pricing[api]['price_usd']

    # 토큰 기반 (OpenAI, Anthropic)
    if api in provider_pricing:
        api_pricing = provider_pricing[api]
        input_cost = (input_tokens / 1_000_000) * api_pricing.get('input_per_1m', 0)
        output_cost = (output_tokens / 1_000_000) * api_pricing.get('output_per_1m', 0)
        return input_cost + output_cost

    return 0.0


def log_api_call(
    provider: str,
    api: str,
    project: str,
    input_tokens: int = 0,
    output_tokens: int = 0,
    pages: int = 0,
    note: str = "",
    cost_usd: Optional[float] = None
) -> Dict[str, Any]:
    """API 호출 로깅"""

    # 비용 계산 (명시되지 않은 경우)
    if cost_usd is None:
        cost_usd = calculate_cost(provider, api, input_tokens, output_tokens, pages)

    record = {
        "timestamp": datetime.now().isoformat(),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "provider": provider,
        "api": api,
        "project": project,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "pages": pages,
        "cost_usd": round(cost_usd, 4),
        "note": note
    }

    # JSONL에 추가
    with open(COST_LOG_PATH, 'a', encoding='utf-8') as f:
        f.write(json.dumps(record, ensure_ascii=False) + '\n')

    return record


def get_logs(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    provider: Optional[str] = None,
    project: Optional[str] = None
) -> list:
    """로그 조회 (필터링)"""
    if not COST_LOG_PATH.exists():
        return []

    logs = []
    with open(COST_LOG_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                record = json.loads(line)

                # 필터링
                if start_date and record['date'] < start_date:
                    continue
                if end_date and record['date'] > end_date:
                    continue
                if provider and record['provider'] != provider:
                    continue
                if project and record['project'] != project:
                    continue

                logs.append(record)

    return logs


def get_daily_summary(date: Optional[str] = None) -> Dict:
    """일별 요약"""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    logs = get_logs(start_date=date, end_date=date)

    summary = {
        "date": date,
        "total_cost_usd": 0,
        "by_provider": {},
        "by_project": {},
        "call_count": len(logs)
    }

    for log in logs:
        cost = log['cost_usd']
        provider = log['provider']
        project = log['project']

        summary['total_cost_usd'] += cost
        summary['by_provider'][provider] = summary['by_provider'].get(provider, 0) + cost
        summary['by_project'][project] = summary['by_project'].get(project, 0) + cost

    summary['total_cost_usd'] = round(summary['total_cost_usd'], 4)
    for k in summary['by_provider']:
        summary['by_provider'][k] = round(summary['by_provider'][k], 4)
    for k in summary['by_project']:
        summary['by_project'][k] = round(summary['by_project'][k], 4)

    return summary


def get_monthly_summary(year_month: Optional[str] = None) -> Dict:
    """월별 요약"""
    if year_month is None:
        year_month = datetime.now().strftime("%Y-%m")

    start_date = f"{year_month}-01"
    # 다음 달 첫날 계산
    year, month = map(int, year_month.split('-'))
    if month == 12:
        end_date = f"{year + 1}-01-01"
    else:
        end_date = f"{year}-{month + 1:02d}-01"

    logs = get_logs(start_date=start_date, end_date=end_date)

    summary = {
        "year_month": year_month,
        "total_cost_usd": 0,
        "by_provider": {},
        "by_project": {},
        "by_date": {},
        "call_count": len(logs)
    }

    for log in logs:
        cost = log['cost_usd']
        provider = log['provider']
        project = log['project']
        date = log['date']

        summary['total_cost_usd'] += cost
        summary['by_provider'][provider] = summary['by_provider'].get(provider, 0) + cost
        summary['by_project'][project] = summary['by_project'].get(project, 0) + cost
        summary['by_date'][date] = summary['by_date'].get(date, 0) + cost

    # 반올림
    summary['total_cost_usd'] = round(summary['total_cost_usd'], 2)
    for k in summary['by_provider']:
        summary['by_provider'][k] = round(summary['by_provider'][k], 2)
    for k in summary['by_project']:
        summary['by_project'][k] = round(summary['by_project'][k], 2)
    for k in summary['by_date']:
        summary['by_date'][k] = round(summary['by_date'][k], 2)

    return summary


def print_summary(summary: Dict):
    """요약 출력"""
    if 'date' in summary:
        print(f"\n=== {summary['date']} 일일 비용 ===")
    elif 'year_month' in summary:
        print(f"\n=== {summary['year_month']} 월간 비용 ===")

    print(f"총 비용: ${summary['total_cost_usd']:.2f}")
    print(f"호출 수: {summary['call_count']}회")

    if summary['by_provider']:
        print("\n[Provider별]")
        for provider, cost in sorted(summary['by_provider'].items(), key=lambda x: -x[1]):
            print(f"  {provider}: ${cost:.2f}")

    if summary['by_project']:
        print("\n[Project별]")
        for project, cost in sorted(summary['by_project'].items(), key=lambda x: -x[1]):
            print(f"  {project}: ${cost:.2f}")


# CLI
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        cmd = sys.argv[1]

        if cmd == "today":
            summary = get_daily_summary()
            print_summary(summary)

        elif cmd == "month":
            year_month = sys.argv[2] if len(sys.argv) > 2 else None
            summary = get_monthly_summary(year_month)
            print_summary(summary)

        elif cmd == "log":
            # 수동 로깅: python cost_tracker.py log upstage document_parse khima --pages 72
            if len(sys.argv) >= 5:
                provider = sys.argv[2]
                api = sys.argv[3]
                project = sys.argv[4]
                pages = 0
                input_tokens = 0
                output_tokens = 0
                note = ""

                i = 5
                while i < len(sys.argv):
                    if sys.argv[i] == "--pages" and i + 1 < len(sys.argv):
                        pages = int(sys.argv[i + 1])
                        i += 2
                    elif sys.argv[i] == "--input" and i + 1 < len(sys.argv):
                        input_tokens = int(sys.argv[i + 1])
                        i += 2
                    elif sys.argv[i] == "--output" and i + 1 < len(sys.argv):
                        output_tokens = int(sys.argv[i + 1])
                        i += 2
                    elif sys.argv[i] == "--note" and i + 1 < len(sys.argv):
                        note = sys.argv[i + 1]
                        i += 2
                    else:
                        i += 1

                record = log_api_call(provider, api, project, input_tokens, output_tokens, pages, note)
                print(f"Logged: {record}")

        else:
            print("Usage:")
            print("  python cost_tracker.py today")
            print("  python cost_tracker.py month [YYYY-MM]")
            print("  python cost_tracker.py log <provider> <api> <project> [--pages N] [--input N] [--output N] [--note 'text']")
    else:
        # 기본: 오늘 요약
        summary = get_daily_summary()
        print_summary(summary)
