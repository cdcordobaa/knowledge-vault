---
type: entity
subtype: agent
created_at: 2026-04-13T21:00:00Z
updated_at: 2026-04-13T21:00:00Z
confidence: high
aliases: [motoko-agent, sales-bot]
relations:
  depends_on: [whatsapp-pipeline]
  generates: [lead-responses]
  measured_by: [b2b-conversion]
  enables: [auto-approval]
  related_to: [b2b-conversion]
---

> **TLDR:** Motoko is an AI-powered sales agent that processes leads from the WhatsApp pipeline and generates automated responses to qualify B2B prospects.

## Overview
[FACT] Motoko is the primary AI agent handling inbound B2B lead qualification. [src: spec-motoko.md]

[FACT] It connects to the WhatsApp pipeline for lead ingestion and uses NLP to classify prospect intent. [src: spec-motoko.md]

[INFERENCE] Motoko's auto-approval flow may introduce risk if not properly gated, as it bypasses human review for certain lead scores. [inferred from: spec-motoko.md, playbook-b2b.md]

## Key Attributes
- **Type:** Sales automation agent
- **Input:** WhatsApp messages via [[whatsapp-pipeline]]
- **Output:** Qualified lead responses
- **Metric:** [[b2b-conversion]] rate

## Open Questions
[GAP] What is the false positive rate for auto-approved leads?
