# Prompt Injection Defense in LLM-Assisted Security Tools

**Course:** Prompt Engineering - MedTech  
**Author:** Mayssa Gloulou & Zeineb Megaadi (junior software engineering students at MedTech SMU)
**Professor:** Abdeldjalil Labed  

---

## Research Overview

This project aims to evaluate the effectiveness of 8 prompt 
design strategies against prompt injection attacks in simulated 
LLM-assisted security tools.

♦ I strongly invite you to check our research paper analyzing these experiments via this link: https://github.com/mayssagl/prompt-injection-research/blob/main/Risks-Of-Prompt-Injection-Research.pdf

Three LLMs were tested:
- Llama 3.3 70B (via Groq
- Gemma2 9B (via Groq)
- Llama 3.1 8B (via Groq)

---

## Key Findings

| Finding | Result |
|---|---|
| Best defense | L8 Fully Hardened (43.3% avg ASR) |
| Worst defense | L7 Chain of Thought (90.0% avg ASR) |
| Gemma2 9B | 100% failure rate on all variants |
| L7 backfire | 35% worse than no protection on Llama 3.3 70B |

---

## Project Structure
prompt-injection-research/
├── config.py              # API settings
├── security_tool.py       # 8 prompt variants + LLM caller
├── attacks.py             # 20 attack inputs + test cases
├── run_experiments.py     # Full experiment runner
├── analyze.py             # Statistics + figure generator
├── results.csv            # Raw experiment results (960 rows)
└── figures/               # All generated graphs
├── asr_chart.png
├── pvalue_heatmap_llama3.3_70b.png
├── pvalue_heatmap_gemma2_9b.png
├── pvalue_heatmap_llama3.1_8b.png
├── false_positive_chart.png
└── miss_rate_chart.png
---

## How to Reproduce Results

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/prompt-injection-research
cd prompt-injection-research
```

### 2. Install dependencies
```bash
pip install groq pandas scipy matplotlib seaborn python-dotenv
```

### 3. Set up API keys
Create a `.env` file:

### 4. Run experiments
```bash
python run_experiments.py
```

### 5. Generate analysis and figures
```bash
python analyze.py
```

---

## Results Summary

### Attack Success Rate (ASR) — Lower is Better

| Variant | Llama 3.3 70B | Llama 3.1 8B | Gemma2 9B | Average |
|---|---|---|---|---|
| L1 No Protection | 55% | 65% | 100% | 75.0% |
| L2 Basic Role | 75% | 70% | 100% | 81.7% |
| L3 Delimiters | 85% | 65% | 100% | 83.3% |
| L4 Explicit Warning | 30% | 85% | 100% | 70.0% |
| L5 Priority Rules | 50% | 70% | 100% | 73.3% |
| L6 Delimiters + Warning | 0% | 45% | 100% | 48.3% |
| L7 Chain of Thought | 90% | 80% | 100% | 90.0% |
| L8 Fully Hardened | 0% | 30% | 100% | 43.3% |

---

## Ethics Statement

This research involves designing and testing prompt injection 
attacks. All experiments were conducted in a controlled 
environment using simulated security tools. No real security 
systems were targeted. Attack inputs are disclosed in the 
appendix to support responsible disclosure and future defense 
research.
