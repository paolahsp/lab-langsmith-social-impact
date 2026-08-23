# Optimization summary

The local A/B comparison shows that the **risk-aware configuration is the best cost/performance trade-off** for deterministic routing: it raises decision accuracy from 80% to 100% on the same 15 cases with zero model tokens, adding only five explicit patterns for subtle measurement and compliance risks. I would use the keyword baseline only for a non-production smoke test, the risk-aware rules for immediate low-cost triage, and the traced evidence-first LLM configuration when briefs vary beyond known patterns or require nuanced explanations; the concise LLM variant is appropriate only if LangSmith confirms comparable hard-case scores at lower token use and latency. Because no API credentials were present in the execution environment, cloud token, latency, and price figures are intentionally not fabricated and must be taken from the two LangSmith runs.

| Configuration | Correct decisions | API tokens | Suitable use |
| --- | ---: | ---: | --- |
| Keyword baseline | 12/15 | 0 | Smoke testing only |
| Risk-aware rules | 15/15 | 0 | Low-cost known-pattern routing |
| Concise LLM | Pending LangSmith run | Pending | Lower-token free-text briefs |
| Evidence-first LLM | Pending LangSmith run | Pending | Nuanced or higher-risk briefs |

