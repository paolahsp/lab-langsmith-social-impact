# Custom evaluator: consulting quality

The custom evaluator measures whether an answer is useful in a consulting workflow rather than merely matching a reference phrase. It returns a continuous score from 0 to 1 using three transparent components: **grounding (45%)**, based on overlap between substantive brief tokens and the answer/action; **actionability (30%)**, based on the presence of an operational verb such as verify, pause, document, approve, review, or escalate; and **format compliance (25%)**, requiring a valid decision plus non-empty answer and next action. A score of 0.75 is the pass threshold. This deterministic evaluator is cheap and reproducible, but lexical overlap cannot detect a sophisticated contradiction, so the cloud experiment also uses OpenEvals' reference-aware LLM judge. The combination separates routing accuracy, workflow usefulness, and semantic correctness instead of hiding them in one score.

## Interpretation

| Score | Meaning |
| ---: | --- |
| `0.75–1.00` | Grounded, actionable, and correctly structured |
| `0.50–0.749` | Usable structure but weak grounding or action |
| `<0.50` | Not safe to rely on without revision |

