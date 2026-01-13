# 작업일지 작성

프로젝트별 작업일지를 작성합니다.

## 일지 위치 규칙

| 프로젝트 | 일지 위치 |
|---------|----------|
| scrape-hub | `C:/Jimin/scrape-hub/meta/journal/YYYY-MM-DD.md` |
| MLAF | `C:/Jimin/MLAF/docs/worklog/YYYY-MM-DD.md` |
| 기타 프로젝트 | `{project}/docs/worklog/YYYY-MM-DD.md` 또는 `{project}/docs/journal/YYYY-MM-DD.md` |

## 파일명 규칙

- **형식**: `YYYY-MM-DD.md` (날짜만, 제목 없음)
- **예시**: `2026-01-13.md`
- 같은 날짜에 여러 작업 → 하나의 파일에 합침
- 제목이나 주제를 파일명에 붙이지 않음

## 일지 템플릿

```markdown
# 작업일지 - YYYY-MM-DD

## 작업 내역

### [프로젝트명] 작업 제목
- 작업 내용 요약
- **결과물**: 경로 또는 설명

## 이슈
- 발생한 문제들 (있으면)

## 다음 할 일
- 예정 작업 (있으면)
```

## 작성 규칙

1. **AI 서명 금지** - "작성: Claude" 같은 표현 사용하지 않음
2. **간결하게** - 핵심만 기록
3. **결과물 링크** - 생성된 파일/문서 경로 명시
4. **이슈 기록** - 문제가 발생했으면 해결 방법과 함께 기록

## 최신 일지 확인

```bash
# scrape-hub
ls -t C:/Jimin/scrape-hub/meta/journal/*.md | head -1

# MLAF
ls -t C:/Jimin/MLAF/docs/worklog/*.md | head -1
```

## 사용 예시

사용자가 `/worklog`를 호출하면:
1. 현재 작업 중인 프로젝트 확인
2. 해당 프로젝트의 일지 위치로 이동
3. 오늘 날짜 파일이 있으면 추가, 없으면 새로 생성
4. 템플릿에 맞춰 작업 내용 기록
