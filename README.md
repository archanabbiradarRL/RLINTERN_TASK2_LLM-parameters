# LLM Parameters Assignment 

## Overview
This project explores how different parameters control the behavior of Large Language Models (LLMs). Through systematic experimentation, we analyze the effects of temperature, top-p/top-k sampling, penalties, and other decoding strategies on model outputs.

## Project Structure
```
LLM_FINAL/
│
├── README.md                 # Project documentation
├── .env                      # Environment variables (API keys)
├── .env.example              # Environment template
├── .gitignore               # Git ignore rules
├── requirements.txt         # Python dependencies
├── generate.py              # CLI tool for parameter testing
├── notebooks/
│   ├── 01_temperature.ipynb
│   ├── 02_top_p_top_k.ipynb
│   ├── 03_penalties.ipynb
│   ├── 04_stop_max_tokens.ipynb
│   ├── 05_beam_search.ipynb
│   └── 06_open_assignment.ipynb
└── outputs/
    ├── temperature_examples.md
    ├── top_p_top_k_examples.md
    ├── penalties_examples.md
    ├── stop_max_tokens_examples.md
    ├── beam_search_examples.md
    └── open_exploration_examples.md
```

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set OpenAI API Key
Create a `.env` file from the template:
```bash
cp .env.example .env
```

Then edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=your_actual_api_key_here
```

### 3. Run Experiments

**Option A - Jupyter Notebooks (Interactive):**
```bash
jupyter notebook
```

**Option B - CLI Tool (Command Line):**
```bash
python generate.py --prompt "Write a story" --temperature 0.8
python generate.py --experiment temperature --prompt "Describe Paris"
python generate.py --help  # See all options
```

## Experiments Overview

### 1. Temperature Experiment (`01_temperature.ipynb`)
- **Purpose**: Explore creativity vs consistency trade-off
- **Parameters**: Temperature values from 0.0 to 1.5
- **Key Finding**: Higher temperature = more creativity, lower consistency

### 2. Top-p/Top-k Sampling (`02_top_p_top_k.ipynb`)
- **Purpose**: Control vocabulary diversity and randomness
- **Parameters**: top_p (0.1-1.0), top_k (1-50)
- **Key Finding**: Fine-grained control over word selection diversity

### 3. Penalties (`03_penalties.ipynb`)
- **Purpose**: Reduce repetition and encourage topic variety
- **Parameters**: frequency_penalty and presence_penalty (0.0-2.0)
- **Key Finding**: Effective for preventing repetitive content

### 4. Stop/Max Tokens (`04_stop_max_tokens.ipynb`)
- **Purpose**: Precise output control and length management
- **Parameters**: stop sequences, max_tokens (50-200)
- **Key Finding**: Essential for structured output control

### 5. Beam Search (`05_beam_search.ipynb`)
- **Purpose**: Balance coherence vs diversity in generation
- **Parameters**: num_beams (1-5), length_penalty (0.5-2.0)
- **Key Finding**: Affects summary quality vs generation speed

### 6. Open Exploration (`06_open_assignment.ipynb`)
- **Purpose**: Advanced parameter techniques
- **Parameters**: logit_bias, JSON mode, seed
- **Key Finding**: Powerful tools for specialized use cases

## CLI Tool Usage

The `generate.py` script provides command-line access to all LLM parameters:

### Quick Examples
```bash
# Single generation with temperature
python generate.py --prompt "Write a story" --temperature 0.8

# Run full temperature experiment
python generate.py --experiment temperature --prompt "Describe Paris"

# Multiple parameters
python generate.py --prompt "List ideas" --top_p 0.9 --frequency_penalty 0.5

# JSON mode
python generate.py --json_mode --prompt "Generate user profile in JSON"

# Reproducible generation
python generate.py --prompt "Random story" --seed 42
```

### Available Parameters
- `--temperature` (-t): Creativity control (0.0-2.0)
- `--top_p`: Nucleus sampling (0.0-1.0)
- `--frequency_penalty`: Reduce repetition (0.0-2.0)
- `--presence_penalty`: Encourage new topics (0.0-2.0)
- `--max_tokens`: Output length limit
- `--stop`: Stop sequences
- `--seed`: Reproducible generation
- `--json_mode`: Force JSON output
- `--experiment`: Run predefined experiments

## Key Findings

### Parameters Most Affecting Creativity
1. **Temperature**: Primary creativity control
2. **Top-p/Top-k**: Secondary creativity through vocabulary diversity
3. **Presence Penalty**: Encourages topic exploration

### Parameters Enforcing Structure
1. **Stop Sequences**: Precise output termination
2. **Max Tokens**: Length control
3. **Low Temperature**: Consistent formatting
4. **High Frequency Penalty**: Prevents repetitive patterns

### Recommended Settings by Use Case

#### Factual Q&A
- Temperature: 0.0-0.3
- Top-p: 0.8-0.9
- Penalties: Low (0.0-0.2)
- **Goal**: Accuracy and consistency

#### Creative Writing
- Temperature: 0.8-1.2
- Top-p: 0.9-1.0
- Presence Penalty: 0.3-0.6
- **Goal**: Novelty and engaging content

#### JSON Output
- Temperature: 0.0-0.1
- Stop sequences: ["}"]
- Max tokens: Limited
- **Goal**: Valid, structured data

## Results

All experiment results are saved in the `outputs/` directory:
- Each experiment generates markdown files with example outputs
- Results show clear parameter effects on model behavior


