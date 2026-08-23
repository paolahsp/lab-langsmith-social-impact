# Evaluation summary

The evaluation used 15 synthetic social-impact consulting briefs across seven categories and three difficulty levels, with a structured target (`decision`, `answer`, `next_action`), exact decision scoring, and a custom 0–1 consulting-quality evaluator; the reproducible local A/B run produced 30 outputs, where the simple keyword configuration achieved **80.0% decision accuracy (12/15)** and the risk-aware configuration achieved **100.0% (15/15)**, while both passed the structural/actionability threshold on all cases. The three baseline failures were hard cases involving an incomplete theory of change, a four-of-80 feedback sample, and an unsigned international-transfer agreement—showing that superficial keyword routing misses implicit evidence-quality and compliance risks. These local results validate the pipeline, not LLM semantic quality; the dataset is synthetic, small, and lexical quality scoring can miss contradictions. The recommended next step is to run both traced OpenAI prompt variants in LangSmith with the OpenEvals judge, then retain the evidence-first configuration only if its hard-case gain justifies its token and latency cost.

| Local configuration | Examples | Decision accuracy | Pass rate |
| --- | ---: | ---: | ---: |
| Keyword baseline | 15 | 80.0% | 80.0% |
| Risk-aware rules | 15 | 100.0% | 100.0% |

