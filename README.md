# Clara Onboarding Automation Pipeline

## Executive Summary

This project simulates Clara’s voice-agent onboarding workflow, transforming unstructured conversations into structured, version-controlled agent configurations.

The system processes:

1. **Demo Call Transcript → v1 Account Memo**
2. **Onboarding Transcript → v2 Account Memo (Patch-Based Update)**

Each version is preserved, and structured diffs are logged to ensure auditability and operational safety.

The design emphasizes modularity, idempotency, and deterministic updates.

---

## System Architecture

```
Demo Transcript
      ↓
Extraction Engine
      ↓
Structured Account Memo (v1)
      ↓
Agent Spec Generation
      ↓
Stored under outputs/accounts/<account_id>/v1

Onboarding Transcript
      ↓
Update Extraction
      ↓
Patch Engine (Dot-Path Updates)
      ↓
Account Memo (v2)
      ↓
Changelog (Field-Level Diff)
      ↓
Agent Spec (v2)
```

---

## Core Design Principles

### 1. Structured Data Modeling

All extracted information is mapped into a predefined JSON schema:

- Metadata
- Company Profile
- Business Hours
- Emergency Triggers
- Routing Rules
- Transfer Protocol
- Integration Constraints
- Unknown Fields

This ensures deterministic behavior and avoids free-form interpretation.

---

### 2. Version-Controlled Evolution

The system distinguishes between:

- **v1 (Exploratory Stage)**  
  Derived from demo conversations.

- **v2 (Operational Stage)**  
  Derived from onboarding clarifications.

The patch engine applies updates selectively without overwriting previous versions.

Example changelog entry:

```json
{
  "field": "business_hours.start_time",
  "previous": "8am",
  "updated": "00:00"
}
```

This provides a transparent audit trail of operational changes.

---

### 3. Idempotent Execution

The pipeline is designed to be safely repeatable:

- Existing `v1` will not be regenerated.
- Existing `v2` will not be overwritten.
- Only explicitly detected updates are applied.
- Missing information is logged instead of inferred.

This ensures operational safety and prevents unintended state mutations.

---

### 4. Deterministic Extraction (No Hallucination Policy)

The system never fabricates information.

If required data is not explicitly present in the transcript, it is:

- Left empty, or
- Added to `questions_or_unknowns`

This prevents unsafe assumptions in production scenarios.

---

## Repository Structure

```
clara-onboarding-automation/
│
├── app.py                     # Streamlit dashboard wrapper
├── README.md
├── requirements.txt
│
├── dataset/
│   ├── demo/                  # Demo transcripts
│   └── onboarding/            # Onboarding transcripts
│
├── outputs/
│   └── accounts/
│       └── <account_id>/
│           ├── v1/
│           │   ├── account_memo.json
│           │   └── agent_spec.json
│           └── v2/
│               ├── account_memo.json
│               ├── agent_spec.json
│               └── changelog.json
│
└── scripts/
    ├── schema.py              # Account schema definition
    ├── extractor.py           # Demo transcript extraction
    ├── versioning.py          # Patch engine & diff logic
    ├── agent_generator.py     # Agent configuration builder
    ├── pipeline_demo.py       # v1 generation pipeline
    └── pipeline_onboarding.py # v2 update pipeline
```

---

## Processing Flow

### Demo Stage (v1)

```
python -m scripts.pipeline_demo
```

- Extracts structured data from demo transcripts.
- Generates v1 account memo.
- Produces initial agent specification.

---

### Onboarding Stage (v2)

```
python -m scripts.pipeline_onboarding <account_id> <transcript_path>
```

- Extracts operational updates.
- Applies structured dot-path patch updates.
- Generates v2 account memo.
- Produces changelog with field-level diffs.

Batch mode is also supported for scalable processing.

---

## Agent Specification Generation

For each account version, the system produces:

- Structured agent metadata
- Business-hour logic
- After-hours routing logic
- Transfer timeout rules
- Retry protocol

The generated JSON structure is compatible with Retell-style agent configurations.

---

## Streamlit Dashboard

A lightweight dashboard (`app.py`) enables:

- Uploading demo transcripts
- Uploading onboarding transcripts
- Viewing v1 and v2 outputs
- Inspecting structured changelogs

This provides a visual interface over the underlying automation engine without modifying backend logic.

---

## Engineering Tradeoffs

- Regex-based extraction is used for deterministic control.
- JSON storage ensures reproducibility.
- No external paid APIs are used.
- The system is fully executable locally.

---

## Production Extension Path

With production infrastructure, this system could be extended to:

- Replace regex extraction with structured LLM extraction layer
- Persist account state in a database (e.g., PostgreSQL)
- Integrate directly with Retell API
- Add structured logging and monitoring
- Provide a diff visualization UI

---

## Conclusion

This project models Clara’s onboarding process as a version-controlled automation system rather than a one-off transformation script.

It prioritizes:

- Structured data modeling
- Controlled updates
- Operational safety
- Auditability
- Reproducibility

The result is a deterministic, modular onboarding automation pipeline suitable for internal deployment.
