# DobbyOps

> A tiny dev-elf for dev work, docs, and cleanup.

개발자를 위한 집요정 도비. Claude Code 스킬 모음집.

## Skills

| Skill | Description |
|-------|-------------|
| `/parse-pdf` | 지능형 PDF 파싱 (PyMuPDF 우선, 필요시 Upstage) |
| `/cost-check` | API 과금 확인 및 로깅 |
| `/worklog` | 프로젝트별 작업일지 작성 |
| `/cleanup` | 시스템 정리 (HF캐시, conda, downloads 등) |

## Install

```powershell
# Clone
git clone https://github.com/sokcho-kim/dobbyops.git
cd dobbyops

# Install (creates symlinks to ~/.claude/commands)
.\install.ps1
```

## Structure

```
dobbyops/
├── commands/           # Claude Code skills
│   ├── parse-pdf.md
│   ├── cost-check.md
│   ├── worklog.md
│   └── cleanup.md
├── shared/             # Shared modules
│   ├── cost_tracker.py
│   ├── parsers.py
│   ├── api_client.py
│   └── config/
│       └── api_pricing.yaml
├── docs/               # Documentation
├── install.ps1         # Install script
└── README.md
```

## Usage

After installation, use skills in any Claude Code session:

```
/parse-pdf    # Parse a PDF file intelligently
/cost-check   # Check API costs
/worklog      # Write work log
/cleanup      # Clean up system
```

## Skill Hierarchy

DobbyOps는 글로벌 스킬입니다. 프로젝트별 스킬과 함께 사용하세요.

```
~/.claude/commands/              ← Global (DobbyOps)
  ├── parse-pdf.md                 범용 스킬
  ├── cost-check.md
  ├── worklog.md
  └── cleanup.md

{project}/.claude/commands/      ← Project-specific
  └── 프로젝트 전용 스킬
```

**예시:**

| Location | Skill | Purpose |
|----------|-------|---------|
| DobbyOps (Global) | `/parse-pdf`, `/worklog` | 범용 |
| scrape-hub | `/hira-scrape` | HIRA 데이터 전용 |
| MLAF | `/na-parse` | 국회법 파싱 전용 |

**우선순위:**
1. 프로젝트 `.claude/commands/` (로컬) - 우선
2. `~/.claude/commands/` (글로벌) - fallback

같은 이름이면 프로젝트 스킬이 우선됩니다.

## Philosophy

**Dobby is free!** But Dobby likes to help.

- **Cost-first**: 무료 도구 우선, 유료는 필요할 때만
- **Track everything**: 모든 유료 API 사용은 기록
- **Keep it simple**: 복잡한 건 싫어요


2026년 1월 24일 (토) @ Naver D2SF

---

*"Dobby has no master. Dobby is a free elf!"*
