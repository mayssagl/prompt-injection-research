# Project Files Overview

## Configuration & Setup

**`config.py`**
Stores shared settings: loads the Groq API key from `.env`, defines the 3 models used in experiments (llama3.3_70b, gemma2_9b, llama3.1_8b), and sets temperature to 0.0.

**`.env`**
Holds all API keys (Groq, Gemini, OpenAI, Anthropic). Never committed to git.

---

## Core Logic

**`security_tool.py`**
The heart of the project. Contains the `run_security_check()` function that sends a system prompt + user input to a model and returns its response. Also defines the 8 prompt variants (L1 to L8), ranging from no protection to fully hardened, and a `prepare_input()` helper that wraps inputs in XML tags for variants that require it.

**`attacks.py`**
A dataset of 40 test inputs split into 3 categories:
- `ATTACK_INPUTS` (20) — injection attempts trying to hijack the tool (role overrides, jailbreaks, disguised commands, prompt leaking)
- `LEGITIMATE_INPUTS` (10) — normal log entries that should always return SAFE
- `THREAT_INPUTS` (10) — real security threats that must return THREAT

---

## Running Experiments

**`run_experiments.py`**
The main experiment runner. Feeds every input from `attacks.py` through every prompt variant × every model (3 × 8 = 24 combinations per input, ~960 total API calls). Scores each response as `failed=1` or `failed=0`, logs everything to `results.csv`.

---

## Testing / Dev Scripts

**`test_apis.py`**
Quick sanity check to verify all 3 API connections are working before running the full experiment.

**`test_variants.py`**
Sends one safe input through all 8 prompt variants on llama3.3_70b. Used to manually inspect how each variant responds before running the full experiment.

**`test_attacks.py`**
Sends the first 3 attack inputs against only L1 (no protection) vs L8 (hardened) to do a quick before/after comparison.

---

## Output

**`results.csv`**
Raw output of `run_experiments.py`. One row per (model, variant, input) combination with columns: model, variant, input_type, input, output, failed.

**`analyze.py`**
Reads `results.csv` and generates 4 figures + a summary printout (see breakdown below).

**`figures/`**
- `asr_chart.png` — Attack Success Rate per variant per model
- `false_positive_chart.png` — How often defenses blocked legitimate inputs
- `miss_rate_chart.png` — How often defenses missed real threats
- `pvalue_heatmap_*.png` — Statistical significance between variants (one per model)