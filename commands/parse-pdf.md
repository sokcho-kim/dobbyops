# PDF 지능형 파싱

대용량 PDF를 비용 효율적으로 파싱합니다.

## 파싱 전략 (4단계)

### 1단계: 파일 확인
- `ls -la` 또는 `dir`로 파일 크기 먼저 확인
- 10MB 이상이면 분할 처리 고려

### 2단계: 무료 도구 우선 (PyMuPDF)
```python
import fitz  # pip install pymupdf

doc = fitz.open("파일.pdf")
# 먼저 3-5페이지만 샘플 테스트
for page_num in range(min(5, len(doc))):
    page = doc[page_num]
    text = page.get_text()
    print(f"=== Page {page_num + 1} ===")
    print(text[:500])  # 미리보기
```

### 3단계: 품질 평가
- 텍스트가 제대로 추출되는가?
- 표/테이블 구조가 유지되는가?
- 한글 깨짐이 없는가?

### 4단계: 선택적 유료 사용
PyMuPDF로 안 되는 부분만 Upstage Document AI 사용
- 스캔 이미지 PDF (OCR 필요)
- 복잡한 표/레이아웃
- 비용: 페이지당 과금 (반드시 cost_tracker로 기록)

## 대용량 파일 처리

**절대 전체 파일을 한번에 열지 않음**

1. 페이지 분할
```python
# 50페이지씩 분할 처리
chunk_size = 50
for start in range(0, len(doc), chunk_size):
    end = min(start + chunk_size, len(doc))
    # 청크 처리
```

2. 결과 병합
- 각 청크 결과를 하나의 파일로 병합
- 페이지 경계에서 문장이 잘리지 않도록 주의

## 사용 예시

사용자가 `/parse-pdf`를 호출하면:
1. 파싱할 PDF 파일 경로 확인
2. 파일 크기 체크
3. 샘플 페이지 테스트
4. 적절한 방법 선택하여 파싱
5. 필요시 과금 기록

## 관련 도구
- PyMuPDF: 무료, 텍스트 기반 PDF에 최적
- Upstage: 유료, OCR/복잡한 레이아웃에 사용
- cost_tracker: 유료 API 사용 시 반드시 기록
