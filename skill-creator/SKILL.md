---
name: skill-creator
description: Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, or optimize a skill's description for better triggering accuracy. This skill works in both WorkBuddy and OpenCode environments.
---

# Skill Creator (OpenCode Edition)

A skill for creating new skills and iteratively improving them, adapted for the OpenCode platform.

## Path Resolution (READ THIS FIRST)

This skill is deployed as a self-contained directory. All bundled resources are located **relative to this SKILL.md file**.

To find the skill directory at runtime:

1. Locate this SKILL.md file. It will be at one of:
   - `~/.config/opencode/skills/skill-creator/SKILL.md` (global install)
   - `.opencode/skills/skill-creator/SKILL.md` (project-level install)
2. The directory containing this SKILL.md is **`$SKILL_DIR`**.

All paths below are relative to `$SKILL_DIR`:

| Resource | Path (relative to `$SKILL_DIR`) |
|----------|-------------------------------|
| Grader template | `agents/grader.md` |
| Comparator template | `agents/comparator.md` |
| Analyzer template | `agents/analyzer.md` |
| JSON schemas | `references/schemas.md` |
| Aggregate benchmark script | `scripts/aggregate_benchmark.py` |
| Generate review script | `eval-viewer/generate_review.py` |
| Validate skill script | `scripts/quick_validate.py` |
| Package skill script | `scripts/package_skill.py` |

When executing Python scripts, use the **absolute path** of `$SKILL_DIR` to form the command. For example:
```bash
python3 $SKILL_DIR/scripts/aggregate_benchmark.py <args>
python3 $SKILL_DIR/eval-viewer/generate_review.py <args>
```

---

## Platform Note

This version is adapted for **OpenCode** (and compatible environments). Key differences from the original Claude Code version:
- **No `claude -p` CLI required for core workflows**: Aggregate, report generation, and review work with standard Python. Trigger eval and description improvement scripts still require Claude Code CLI but are optional — use the manual/guided workflows instead.
- **No dynamic subagent prompts**: Grader, Comparator, Analyzer run as inline prompt templates rather than spawned subagents with custom agent files
- **Static HTML viewer**: Uses `--static` mode instead of `webbrowser.open()`
- **Serial execution**: Test cases run one at a time instead of parallel subagent spawning
- **Python 3.7+ compatible**: All scripts use `typing` module instead of PEP 585 syntax

At a high level, the process of creating a skill goes like this:

- Decide what you want the skill to do and roughly how it should do it
- Write a draft of the skill
- Create a few test prompts and run the skill on them
- Help the user evaluate the results both qualitatively and quantitatively
  - While the runs happen, draft some quantitative evals (or use existing ones)
  - Use the `eval-viewer/generate_review.py` script to show the user the results
- Rewrite the skill based on feedback
- Repeat until you're satisfied
- Expand the test set and try again at larger scale

## Communicating with the user

The skill creator is liable to be used by people across a wide range of familiarity with coding jargon. Please pay attention to context cues to understand how to phrase your communication! In the default case:
- "evaluation" and "benchmark" are borderline, but OK
- for "JSON" and "assertion" you want to see serious cues from the user that they know what those things are before using them without explaining them

It's OK to briefly explain terms if you're in doubt, and feel free to clarify terms with a short definition if you're unsure if the user will get it.

---

## Creating a skill

### Capture Intent

Start by understanding the user's intent. The current conversation might already contain a workflow the user wants to capture. If so, extract answers from the conversation history first.

1. What should this skill enable the agent to do?
2. When should this skill trigger? (what user phrases/contexts)
3. What's the expected output format?
4. Should we set up test cases to verify the skill works? Skills with objectively verifiable outputs benefit from test cases. Suggest the appropriate default based on the skill type, but let the user decide.

### Interview and Research

Proactively ask questions about edge cases, input/output formats, example files, success criteria, and dependencies. Wait to write test prompts until you've got this part ironed out.

### Write the SKILL.md

Based on the user interview, fill in these components:

- **name**: Skill identifier (kebab-case)
- **description**: When to trigger, what it does. Include both what the skill does AND specific contexts for when to use it. Make the description a little bit "pushy" to combat undertriggering.
- **compatibility**: Required tools, dependencies (optional, rarely needed)
- **the rest of the skill :)**

### Skill Writing Guide

#### Anatomy of a Skill

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description required)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/    - Executable code for deterministic/repetitive tasks
    ├── references/ - Docs loaded into context as needed
    └── assets/     - Files used in output (templates, icons, fonts)
```

#### Progressive Disclosure

Skills use a three-level loading system:
1. **Metadata** (name + description) - Always in context (~100 words)
2. **SKILL.md body** - In context whenever skill triggers (<500 lines ideal)
3. **Bundled resources** - As needed (unlimited, scripts can execute without loading)

**Key patterns:**
- Keep SKILL.md under 500 lines
- Reference files clearly from SKILL.md with guidance on when to read them
- For large reference files (>300 lines), include a table of contents

#### Writing Patterns

Prefer using the imperative form in instructions.

**Defining output formats**:
```markdown
## Report structure
ALWAYS use this exact template:
# [Title]
## Executive summary
## Key findings
## Recommendations
```

**Examples pattern**:
```markdown
## Commit message format
**Example 1:**
Input: Added user authentication with JWT tokens
Output: feat(auth): implement JWT-based authentication
```

### Writing Style

Try to explain to the model why things are important in lieu of heavy-handed musty MUSTs. Use theory of mind and try to make the skill general and not super-narrow to specific examples.

### Test Cases

After writing the skill draft, come up with 2-3 realistic test prompts. Share them with the user: "Here are a few test cases I'd like to try. Do these look right, or do you want to add more?"

Save test cases to `evals/evals.json`. Don't write assertions yet — just the prompts.

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "User's task prompt",
      "expected_output": "Description of expected result",
      "files": []
    }
  ]
}
```

See `references/schemas.md` for the full schema.

---

## Running and evaluating test cases

This section is one continuous sequence — don't stop partway through. Do NOT use any other testing skill.

Put results in `<skill-name>-workspace/` as a sibling to the skill directory. Within the workspace, organize results by iteration (`iteration-1/`, `iteration-2/`, etc.) and within that, each test case gets a directory (`eval-0/`, `eval-1/`, etc.).

### Step 1: Execute test cases (serial, with skill AND baseline)

Since OpenCode does not support parallel subagent spawning with custom prompts, execute test cases **serially**:

For each test case:
1. **With-skill run**: Follow the skill's instructions to accomplish the eval prompt yourself. Save outputs to `<workspace>/iteration-<N>/eval-<ID>/with_skill/outputs/`.
2. **Baseline run** (same prompt, no skill):
   - **Creating a new skill**: accomplish the same task without the skill. Save to `without_skill/outputs/`.
   - **Improving an existing skill**: snapshot the old skill first (`cp -r <skill-path> <workspace>/skill-snapshot/`), then accomplish the task with the old skill. Save to `old_skill/outputs/`.

Write an `eval_metadata.json` for each test case:

```json
{
  "eval_id": 0,
  "eval_name": "descriptive-name-here",
  "prompt": "The user's task prompt",
  "assertions": []
}
```

### Step 2: Draft assertions

After running all test cases, draft quantitative assertions. Good assertions are objectively verifiable and have descriptive names.

Update `eval_metadata.json` files and `evals/evals.json` with the assertions.

### Step 3: Capture timing data

Record wall-clock time for each run manually and save to `timing.json`:

```json
{
  "total_duration_seconds": 23.3,
  "executor_duration_seconds": 23.3,
  "executor_start": "2026-01-15T10:30:00Z",
  "executor_end": "2026-01-15T10:32:45Z"
}
```

If you have access to token count information, include `total_tokens` as well.

### Step 4: Grade, aggregate, and launch the viewer

Once all runs are done:

1. **Grade each run** — Read and apply the Grader prompt template from `$SKILL_DIR/agents/grader.md` inline. Read the transcript and outputs, evaluate each assertion, and save results to **`<outputs_dir>/grading.json`** (i.e. `eval-<ID>/with_skill/outputs/grading.json` or `eval-<ID>/without_skill/outputs/grading.json`). The grading.json expectations array must use the fields `text`, `passed`, and `evidence`. For assertions that can be checked programmatically, write and run a script rather than eyeballing it.

2. **Aggregate into benchmark** — run the aggregation script:
   ```bash
   python3 $SKILL_DIR/scripts/aggregate_benchmark.py <workspace>/iteration-N --skill-name <name>
   ```
   This produces `benchmark.json` and `benchmark.md`.

3. **Do an analyst pass** — Read and apply the Analyzer prompt template from `$SKILL_DIR/agents/analyzer.md` inline. Surface patterns the aggregate stats might hide.

4. **Launch the viewer** with static HTML output:
   ```bash
   python3 $SKILL_DIR/eval-viewer/generate_review.py <workspace>/iteration-N \
     --skill-name "my-skill" \
     --benchmark <workspace>/iteration-N/benchmark.json \
     --static <workspace>/iteration-N/review.html
   ```
   For iteration 2+, also pass `--previous-workspace <workspace>/iteration-<N-1>`.

   The resulting HTML file can be opened in any browser.

5. **Tell the user**: "I've generated a review page at `<path>`. Open it in your browser. There are two tabs — 'Outputs' lets you click through each test case, 'Benchmark' shows the quantitative comparison. Leave feedback in the textbox for each test case. When you're done, come back here."

### Step 5: Read the feedback

When the user tells you they're done, read the feedback they provide (either from the HTML viewer's feedback export, or directly from the conversation).

---

## Improving the skill

### How to think about improvements

1. **Generalize from the feedback.** Don't overfit to specific examples. Try different metaphors, different patterns of working.
2. **Keep the prompt lean.** Remove things that aren't pulling their weight. Look at the transcripts — if the skill makes the model waste time, trim those parts.
3. **Explain the why.** Use theory of mind. If you find yourself writing ALWAYS or NEVER in all caps, reframe and explain the reasoning instead.
4. **Look for repeated work across test cases.** If all test cases resulted in writing similar helper scripts, bundle that script into `scripts/`.

### The iteration loop

After improving the skill:

1. Apply your improvements to the skill
2. Re-execute all test cases into a new `iteration-<N+1>/` directory
3. Regenerate the viewer with `--previous-workspace`
4. Wait for the user to review
5. Read feedback, improve again, repeat

Keep going until:
- The user says they're happy
- The feedback is all empty (everything looks good)
- You're not making meaningful progress

---

## Advanced: Blind comparison

For situations where you want a more rigorous comparison between two versions of a skill. Read and apply the Comparator prompt template from `$SKILL_DIR/agents/comparator.md` inline to judge which output is better without knowing which skill produced it.

This is optional and most users won't need it. The human review loop is usually sufficient.

---

## Description Optimization (Manual / Guided)

Since OpenCode lacks `claude -p` CLI, the automated trigger eval loop is not available. Instead, use this guided manual approach:

### Step 1: Generate trigger eval queries

Create 20 eval queries — a mix of should-trigger and should-not-trigger. Save as JSON:

```json
[
  {"query": "the user prompt", "should_trigger": true},
  {"query": "another prompt", "should_trigger": false}
]
```

For **should-trigger** queries (8-10): different phrasings of the same intent, some formal, some casual. Include edge cases.

For **should-not-trigger** queries (8-10): near-misses that share keywords but actually need something different.

### Step 2: Review with user

Present the eval set to the user. They can edit queries, toggle should-trigger, add/remove entries.

### Step 3: Manual trigger testing

For each query, simulate what would happen:
1. Show the user the query and the current skill description
2. Ask: "Would this description make an agent load this skill for this query?"
3. Record the result as `triggered: true/false`

### Step 4: Improve based on failures

For queries that failed (should trigger but didn't, or vice versa), manually revise the description. Focus on:
- Generalizing from failures to broader intent categories (not overfitting to specific phrasings)
- Keeping under 1024 characters
- Using imperative phrasing ("Use this skill for...")
- Making it distinctive and immediately recognizable

Iterate until the user is satisfied with the trigger accuracy.

---

## OpenCode Deployment

### Directory Layout

```
~/.config/opencode/
├── agents/
│   ├── skill-executor.md       # /skill-eval execution agent (primary)
│   └── skill-grader.md         # /skill-eval grading agent (subagent, read-only)
├── commands/
│   ├── skill-create.md         # /skill-create command
│   ├── skill-eval.md           # /skill-eval command
│   └── skill-improve.md        # /skill-improve command
└── skills/
    └── skill-creator/
        ├── SKILL.md            ← THIS FILE (main skill definition)
        ├── agents/             # Prompt templates (grader, comparator, analyzer)
        ├── scripts/            # Python utilities (aggregate_benchmark, etc.)
        ├── eval-viewer/        # HTML review page generator
        ├── references/         # JSON schemas
        └── docs/               # Documentation
```

**Commands and agents** go in `~/.config/opencode/agents/` and `~/.config/opencode/commands/` (global) or `.opencode/agents/` and `.opencode/commands/` (project-level).

**Everything else** (SKILL.md, agents/, scripts/, eval-viewer/, references/) lives under `~/.config/opencode/skills/skill-creator/`. All internal paths in SKILL.md are relative to this directory.

---

## Reference files

The `agents/` directory contains **prompt templates** (not Claude Code agent definitions). Read them and apply inline when needed:

- `agents/grader.md` — How to evaluate assertions against outputs
- `agents/comparator.md` — How to do blind A/B comparison between two outputs
- `agents/analyzer.md` — How to analyze benchmark results

The `references/` directory has additional documentation:
- `references/schemas.md` — JSON structures for evals.json, grading.json, etc.

The `scripts/` directory contains Python utilities (no `claude -p` dependency for OpenCode-used scripts):
- `scripts/aggregate_benchmark.py` — Aggregate grading results into benchmark.json
- `scripts/generate_report.py` — Generate HTML report from run_loop output
- `scripts/quick_validate.py` — Validate SKILL.md format
- `scripts/package_skill.py` — Package skill into .skill file
- `scripts/utils.py` — Shared utilities
- `scripts/run_eval.py` — Trigger evaluation (requires Claude Code CLI)
- `scripts/improve_description.py` — Improve description from eval results (requires Claude Code CLI)
- `scripts/run_loop.py` — Eval + improve loop (requires Claude Code CLI)

---

Repeating the core loop for emphasis:

- Figure out what the skill is about
- Draft or edit the skill
- Run the skill on test prompts (serially)
- With the user, evaluate the outputs:
  - Create benchmark.json and generate static HTML review page
  - Run quantitative evals
- Repeat until you and the user are satisfied
- Package the final skill and return it to the user.
