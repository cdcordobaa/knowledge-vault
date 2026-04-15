---
type: entity
subtype: product
created_at: 2026-04-13T21:00:00Z
updated_at: 2026-04-13T21:00:00Z
confidence: high
aliases: [wa-pipeline, whatsapp-ingestion]
relations:
  generates: [motoko]
  enables: [b2b-conversion]
  related_to: [motoko]
---

> **TLDR:** The WhatsApp Pipeline ingests leads from WhatsApp Business API, normalizes messages, and routes them to downstream agents like Motoko for qualification.

## Overview
[FACT] The pipeline handles message ingestion, deduplication, and routing from the WhatsApp Business API. [src: sales-report.md]

[FACT] It processes an average of 500 messages per day during peak hours. [src: sales-report.md]

[INFERENCE] Pipeline latency directly impacts Motoko's response time, which correlates with conversion rates. [inferred from: sales-report.md, playbook-b2b.md]

## Key Attributes
- **Input:** WhatsApp Business API webhooks
- **Output:** Normalized lead objects routed to [[motoko]]
- **Volume:** ~500 messages/day peak

## Open Questions
[GAP] What happens when the pipeline goes down — is there a dead-letter queue?
