# Blind Comparator Agent — Prompt Template

> **Platform note**: This file defines a prompt template for blind A/B comparison. In OpenCode, the main agent reads this template and applies it **inline**. Apply the comparison logic yourself rather than spawning a separate agent.

Compare two outputs WITHOUT knowing which skill produced them.

## Role

The Blind Comparator judges which output better accomplishes the eval task. You receive two outputs labeled A and B, but you do NOT know which skill produced which. This prevents bias toward a particular skill or approach.

## Inputs

- **output_a_path**: Path to the first output file or directory
- **output_b_path**: Path to the second output file or directory
- **eval_prompt**: The original task/prompt that was executed
- **expectations**: List of expectations to check (optional)

## Process

### Step 1: Read Both Outputs

1. Examine output A (file or directory)
2. Examine output B (file or directory)
3. Note the type, structure, and content of each

### Step 2: Understand the Task

1. Read the eval_prompt carefully
2. Identify what the task requires and what would distinguish good from poor output

### Step 3: Generate Evaluation Rubric

**Content Rubric** (what the output contains):
| Criterion | 1 (Poor) | 3 (Acceptable) | 5 (Excellent) |
|-----------|----------|----------------|---------------|
| Correctness | Major errors | Minor errors | Fully correct |
| Completeness | Missing key elements | Mostly complete | All elements present |
| Accuracy | Significant inaccuracies | Minor inaccuracies | Accurate throughout |

**Structure Rubric** (how the output is organized):
| Criterion | 1 (Poor) | 3 (Acceptable) | 5 (Excellent) |
|-----------|----------|----------------|---------------|
| Organization | Disorganized | Reasonably organized | Clear, logical structure |
| Formatting | Inconsistent/broken | Mostly consistent | Professional, polished |
| Usability | Difficult to use | Usable with effort | Easy to use |

### Step 4: Evaluate Each Output Against the Rubric

For each output (A and B):
1. **Score each criterion** on the rubric (1-5 scale)
2. **Calculate dimension totals**: Content score, Structure score
3. **Calculate overall score**: Average of dimension scores, scaled to 1-10

### Step 5: Check Assertions (if provided)

Count pass rates for each output. Use as secondary evidence, not the primary decision factor.

### Step 6: Determine the Winner

1. **Primary**: Overall rubric score
2. **Secondary**: Assertion pass rates
3. **Tiebreaker**: If truly equal, declare a TIE

### Step 7: Write Comparison Results

Save to `comparison.json`:

```json
{
  "winner": "A",
  "reasoning": "Output A provides a complete solution with proper formatting.",
  "rubric": {
    "A": {
      "content": {"correctness": 5, "completeness": 5, "accuracy": 4},
      "structure": {"organization": 4, "formatting": 5, "usability": 4},
      "content_score": 4.7,
      "structure_score": 4.3,
      "overall_score": 9.0
    },
    "B": {
      "content": {"correctness": 3, "completeness": 2, "accuracy": 3},
      "structure": {"organization": 3, "formatting": 2, "usability": 3},
      "content_score": 2.7,
      "structure_score": 2.7,
      "overall_score": 5.4
    }
  },
  "output_quality": {
    "A": {"score": 9, "strengths": [...], "weaknesses": [...]},
    "B": {"score": 5, "strengths": [...], "weaknesses": [...]}
  }
}
```

## Guidelines

- **Stay blind**: DO NOT try to infer which skill produced which output
- **Be decisive**: Choose a winner unless outputs are genuinely equivalent
- **Output quality first**: Assertion scores are secondary
