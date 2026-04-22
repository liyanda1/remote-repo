# Post-hoc Analyzer Agent — Prompt Template

> **Platform note**: This file defines a prompt template for benchmark analysis. In OpenCode, the main agent reads this template and applies it **inline**. Contains two sections: blind comparison analysis and benchmark results analysis.

---

## Part A: Blind Comparison Analysis

Analyze blind comparison results to understand WHY the winner won.

### Inputs

- **winner**: "A" or "B"
- **winner_skill_path**: Path to the winning skill
- **winner_transcript**: Execution log for the winner
- **loser_skill_path**: Path to the losing skill
- **loser_transcript**: Execution log for the loser

### Process

1. **Read Comparison Result** — Note the winning side and reasoning
2. **Read Both Skills** — Identify structural differences in instructions, scripts, examples, edge cases
3. **Read Both Transcripts** — Compare execution patterns, tool usage, divergence points
4. **Analyze Instruction Following** — Score 1-10 for each side
5. **Identify Winner Strengths** — Be specific, quote from skills/transcripts
6. **Identify Loser Weaknesses** — What held the loser back?
7. **Generate Improvement Suggestions** — Prioritize by impact (high/medium/low)

### Output Format

Save to `analysis.json`:

```json
{
  "comparison_summary": {
    "winner": "A",
    "winner_skill": "path/to/winner/skill",
    "loser_skill": "path/to/loser/skill",
    "comparator_reasoning": "Brief summary"
  },
  "winner_strengths": ["Clear step-by-step instructions", ...],
  "loser_weaknesses": ["Vague instruction led to inconsistency", ...],
  "instruction_following": {
    "winner": {"score": 9, "issues": [...]},
    "loser": {"score": 6, "issues": [...]}
  },
  "improvement_suggestions": [
    {
      "priority": "high",
      "category": "instructions",
      "suggestion": "Replace vague instruction with explicit steps",
      "expected_impact": "Would eliminate ambiguity"
    }
  ],
  "transcript_insights": {
    "winner_execution_pattern": "Read skill -> Followed process -> Used script",
    "loser_execution_pattern": "Read skill -> Unclear on approach -> Tried 3 methods"
  }
}
```

### Categories for Suggestions

| Category | Description |
|----------|-------------|
| `instructions` | Changes to the skill's prose instructions |
| `tools` | Scripts, templates, or utilities to add/modify |
| `examples` | Example inputs/outputs to include |
| `error_handling` | Guidance for handling failures |
| `structure` | Reorganization of skill content |
| `references` | External docs or resources to add |

---

## Part B: Analyzing Benchmark Results

Review benchmark data and generate freeform notes that help the user understand skill performance.

### Inputs

- **benchmark_data_path**: Path to benchmark.json
- **output_path**: Where to save the notes

### Process

1. **Read Benchmark Data** — Note configurations and aggregates
2. **Analyze Per-Assertion Patterns**:
   - Always pass both configs? (non-discriminating)
   - Always fail both? (broken or beyond capability)
   - Always pass with skill, fail without? (clear value)
   - Highly variable? (flaky)
3. **Analyze Cross-Eval Patterns** — Consistent difficulty levels, high variance evals, surprises
4. **Analyze Metrics Patterns** — Time/token overhead, outliers
5. **Generate Notes** — Each note should state a specific observation grounded in data

### Output

Save notes as JSON array of strings:

```json
[
  "Assertion 'Output is a PDF file' passes 100% in both configurations - may not differentiate skill value",
  "Eval 3 shows high variance (50% ± 40%) - run 2 had an unusual failure",
  "Without-skill runs consistently fail on table extraction expectations"
]
```

### Guidelines

**DO**: Report what you observe, be specific, note patterns aggregates hide, provide context.

**DO NOT**: Suggest improvements (that's for the improvement step), make subjective quality judgments, speculate without evidence, repeat aggregate stats.
