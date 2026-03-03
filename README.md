# Clara Voice Agent Automation Pipeline

## Overview

This project simulates Clara’s onboarding automation challenge:

Demo Call → Structured Account Memo (v1) → Agent Draft  
Onboarding Update → Patch Engine → Versioned Agent (v2)

The system converts unstructured human conversation into structured operational rules and deployable AI agent configurations.

The architecture is designed to be:

- Modular  
- Version-controlled  
- Idempotent  
- Batch-capable  
- Zero-cost and reproducible  

This project is intentionally built to feel like a small internal automation product rather than a one-off script.

---

## 🧠 Architecture

```
Transcript (Demo)
        ↓
Extractor Engine
        ↓
Account Memo (v1 JSON)
        ↓
Agent Spec Generator
        ↓
Stored under outputs/accounts/<account_id>/v1

Onboarding Transcript
        ↓
Patch Extractor
        ↓
Versioning Engine
        ↓
Account Memo (v2 JSON)
        ↓
Agent Spec (v2)
        ↓
Changelog (diff log)
```

---

## 🗂 Folder Structure

```
dataset/
 ├── demo/
 └── onboarding/

outputs/
 └── accounts/
     └── <account_id>/
         ├── v1/
         │   ├── account_memo.json
         │   └── agent_spec.json
         └── v2/
             ├── account_memo.json
             ├── agent_spec.json
             └── changelog.json

scripts/
 ├── schema.py
 ├── extractor.py
 ├── agent_generator.py
 ├── versioning.py
 ├── pipeline_demo.py
 └── pipeline_onboarding.py
```

---

## 🧾 Account Memo Design

The Account Memo JSON is structured to separate:

- Metadata (version, timestamps, source)
- Company profile
- Business hours
- Services & emergency triggers
- Routing rules
- Transfer rules
- Integration constraints
- Unknown or missing fields

No assumptions are made beyond what is explicitly detected.

If information is missing, it is recorded under:

```
questions_or_unknowns
```

This ensures no hallucination and preserves operational safety.

---

## 🔄 Versioning Strategy

### v1:
- Generated from demo call transcript.
- Represents exploratory understanding.

### v2:
- Generated from onboarding transcript.
- Applies structured updates using a patch engine.
- Does NOT overwrite v1.
- Logs all modifications in `changelog.json`.

Example changelog entry:

```json
{
  "field": "business_hours.start_time",
  "previous": "8am",
  "updated": "00:00"
}
```

This provides auditability and controlled evolution.

---

## ⚙️ Idempotency & Safety

The system prevents accidental overwrites:

- If v1 exists → it is not regenerated.
- If v2 exists → onboarding update is skipped.
- Patch engine updates only explicitly changed fields.

This makes the pipeline repeatable and safe to run in batch mode.

---

## 📦 Batch Processing

### Demo transcripts:
```
python scripts/pipeline_demo.py
```

### Onboarding transcripts  
(Named as `account_<account_id>.txt`):
```
python scripts/pipeline_onboarding.py
```

The onboarding pipeline prints a summary:

- processed
- success
- already_exists
- no_updates
- missing_v1

This simulates scalable automation across multiple accounts.

---

## 🤖 Agent Spec Generation

For each account version:

- Agent name is dynamically generated.
- Business hours are injected.
- Transfer protocol is structured.
- Prompt includes required conversation flows:
  - Business hours flow
  - After-hours flow
  - Transfer and fallback handling

The generated agent spec is compatible with Retell-style configuration JSON.

---

## 🧠 Missing Data Strategy

The system never fabricates information.

If fields are not explicitly present in transcript:

- They are left blank
- Or added to `questions_or_unknowns`

This prevents unsafe operational assumptions.

---

## 🛠 Engineering Decisions

- Modular design (schema, extraction, generation, versioning separated)
- Dot-path patch logic for nested updates
- JSON-based storage for reproducibility
- CLI-based execution
- Zero paid APIs
- Fully local execution

---

## 🔮 Future Improvements (Production Context)

With production access:

- Replace regex extraction with structured LLM extraction layer
- Add database persistence (PostgreSQL/Supabase)
- Add diff viewer UI
- Integrate directly with Retell APIs
- Add retry logic + structured logging

---

## 🎥 Demo Flow

1. Show demo transcript → v1 generation  
2. Show onboarding transcript → v2 generation  
3. Open changelog  
4. Explain version evolution  

---

## 🎯 Design Philosophy

This project treats onboarding automation as a version-controlled system rather than a one-off transformation.

It emphasizes:

- Structured data modeling
- Controlled updates
- Operational safety
- Reproducibility
- Clean system boundaries

---

## 🚀 Result

This pipeline simulates Clara’s real-world onboarding automation:

Messy conversation → structured operational rules → deployable AI agent spec.