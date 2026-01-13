# 시스템 정리

C 드라이브 용량 확보 및 시스템 정리를 수행합니다.

## 정리 대상

### 1. Huggingface 캐시
```bash
# 캐시 위치 확인
ls -la C:/Users/sokch/.cache/huggingface/hub/

# 용량 확인
du -sh C:/Users/sokch/.cache/huggingface/hub/*
```

**정리 기준:**
- 6개월 이상 미사용 모델
- 중복 다운로드된 모델
- 더 이상 필요 없는 실험용 모델

### 2. Conda 환경 (uv로 전환)
```bash
# conda 환경 목록
conda env list

# 환경 삭제
conda env remove -n <env_name>
```

### 3. Downloads 폴더
```powershell
# 설치파일 확인
Get-ChildItem C:/Users/sokch/Downloads -Filter "*.exe" | Sort-Object Length -Descending
Get-ChildItem C:/Users/sokch/Downloads -Filter "*.msi" | Sort-Object Length -Descending

# 중복 파일 확인 (이름에 (1), (2) 포함)
Get-ChildItem C:/Users/sokch/Downloads | Where-Object { $_.Name -match '\(\d+\)' }
```

### 4. Claude Code 임시 파일
```bash
# 프로젝트 루트의 tmpclaude 파일 확인
find C:/Jimin -maxdepth 2 -name "tmpclaude-*" -type f 2>/dev/null

# 삭제
find C:/Jimin -maxdepth 2 -name "tmpclaude-*" -type f -delete 2>/dev/null
```

**정리 기준:**
- `tmpclaude-*` 패턴의 모든 파일 삭제
- 세션 종료 후 남은 임시 파일

> `.gitignore`에 `tmpclaude-*` 패턴 추가 권장

### 5. Git 레포지토리
```bash
# C:/Jimin 레포 목록
ls -la C:/Jimin/

# 각 레포 크기 확인
du -sh C:/Jimin/*/
```

**정리 기준:**
- 마지막 커밋이 6개월 이상 전
- 원격 저장소와 동기화된 백업 레포
- 완료된 대회/프로젝트

## 정리 로그 위치

- `C:/Jimin/maintenance/logs/YYYY-MM-DD_cleanup.md`

## 정리 스크립트

| 스크립트 | 용도 |
|---------|------|
| `check_size.ps1` | 폴더별 용량 확인 |
| `check_hf.ps1` | Huggingface 캐시 확인 |
| `check_conda.ps1` | Conda 환경 확인 |
| `check_downloads.ps1` | Downloads 폴더 확인 |
| `check_cache.ps1` | 기타 캐시 확인 |

## 이전 정리 결과 참조

`C:/Jimin/maintenance/logs/2026-01-06_cleanup.md`:
- 레포 정리: ~7 GB
- Huggingface 캐시: ~38 GB
- Conda 환경: ~15 GB
- Downloads 정리: ~7 GB
- **총 67 GB 확보**

## 사용 예시

사용자가 `/cleanup`를 호출하면:
1. 현재 C 드라이브 용량 확인
2. 정리 대상별 용량 분석
3. 삭제 대상 목록 제시 (확인 후 삭제)
4. 정리 결과를 로그에 기록
