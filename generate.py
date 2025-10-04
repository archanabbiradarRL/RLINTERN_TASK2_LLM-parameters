#!/usr/bin/env python3
"""
LLM Parameters CLI Tool

A command-line interface for testing different LLM parameters with OpenAI API.
Supports all major parameters: temperature, top_p, top_k, penalties, stop sequences, and more.

Usage Examples:
    python generate.py --prompt "Write a story" --temperature 0.8
    python generate.py --experiment temperature --prompt "Describe Paris"
    python generate.py --top_p 0.9 --top_k 50 --prompt "List synonyms for happy"
    python generate.py --json_mode --prompt "Generate a user profile"
"""

import argparse
import sys
import os
from datetime import datetime
from openai import OpenAI

# Initialize OpenAI client with error handling
def get_openai_client():
    api_key = "your api key"
    
    try:
        # Try with the API key directly
        return OpenAI(api_key=api_key)
    except Exception as e:
        print(f" Error initializing OpenAI client: {e}")
        print(" Try upgrading OpenAI library: pip install --upgrade openai")
        sys.exit(1)

client = get_openai_client()

def save_to_md(content, experiment_type="Single Generation", prompt="", timestamp=None):
    """Save output to generate_py.md file."""
    if timestamp is None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    md_content = f"""
## {experiment_type}
**Timestamp:** {timestamp}
**Prompt:** {prompt}

{content}

---
"""
    
    try:
        with open("generate_py.md", "a", encoding="utf-8") as f:
            f.write(md_content)
        print(f" Output saved to generate_py.md")
    except Exception as e:
        print(f" Could not save to file: {e}")

def run_temperature_experiment(prompt):
    """Run temperature experiment with multiple values."""
    temperatures = [0.0, 0.5, 1.0, 1.5]
    results = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f" Temperature Experiment: '{prompt}'\n")
    
    md_output = f"### Temperature Experiment Results\n"
    
    for temp in temperatures:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=temp,
            max_tokens=200
        )
        
        output = response.choices[0].message.content
        results.append(f"Temperature {temp}: {output}")
        print(f" Temperature {temp}:")
        print(f"   {output}\n")
        
        md_output += f"\n**Temperature {temp}:**\n{output}\n"
    
    # Save to markdown file
    save_to_md(md_output, "Temperature Experiment", prompt, timestamp)
    
    return results

def run_top_p_experiment(prompt):
    """Run top-p experiment with different nucleus sampling values."""
    top_p_values = [0.1, 0.5, 0.9, 1.0]
    results = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f" Top-p Experiment: '{prompt}'\n")
    
    md_output = f"### Top-p Experiment Results\n"
    
    for top_p in top_p_values:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            top_p=top_p,
            temperature=0.8,
            max_tokens=200
        )
        
        output = response.choices[0].message.content
        results.append(f"Top-p {top_p}: {output}")
        print(f" Top-p {top_p}:")
        print(f"   {output}\n")
        
        md_output += f"\n**Top-p {top_p}:**\n{output}\n"
    
    # Save to markdown file
    save_to_md(md_output, "Top-p Experiment", prompt, timestamp)
    
    return results

def run_penalties_experiment(prompt):
    """Run penalties experiment with frequency and presence penalties."""
    penalty_configs = [
        {"freq": 0.0, "pres": 0.0, "label": "No Penalties"},
        {"freq": 1.0, "pres": 0.0, "label": "Frequency Penalty"},
        {"freq": 0.0, "pres": 1.0, "label": "Presence Penalty"},
        {"freq": 0.5, "pres": 0.5, "label": "Both Penalties"}
    ]
    
    print(f" Penalties Experiment: '{prompt}'\n")
    results = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    md_output = f"### Penalties Experiment Results\n"
    
    for config in penalty_configs:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            frequency_penalty=config["freq"],
            presence_penalty=config["pres"],
            temperature=0.7,
            max_tokens=200
        )
        
        output = response.choices[0].message.content
        results.append(f"{config['label']}: {output}")
        print(f"{config['label']}:")
        print(f"   {output}\n")
        
        md_output += f"\n**{config['label']}** (freq: {config['freq']}, pres: {config['pres']}):\n{output}\n"
    
    # Save to markdown file
    save_to_md(md_output, "Penalties Experiment", prompt, timestamp)
    
    return results

def generate_single(args):
    """Generate a single response with specified parameters."""
    
    # Handle JSON mode - modify prompt if needed
    prompt = args.prompt
    if args.json_mode and "json" not in prompt.lower():
        prompt = f"{args.prompt} Please respond in JSON format."
    
    # Build the API call parameters
    api_params = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": args.max_tokens
    }
    
    # Add optional parameters if specified
    if args.temperature is not None:
        api_params["temperature"] = args.temperature
    if args.top_p is not None:
        api_params["top_p"] = args.top_p
    if args.frequency_penalty is not None:
        api_params["frequency_penalty"] = args.frequency_penalty
    if args.presence_penalty is not None:
        api_params["presence_penalty"] = args.presence_penalty
    if args.stop:
        api_params["stop"] = args.stop
    if args.seed is not None:
        api_params["seed"] = args.seed
    if args.json_mode:
        api_params["response_format"] = {"type": "json_object"}
    
    # Make the API call
    try:
        response = client.chat.completions.create(**api_params)
        output = response.choices[0].message.content
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Display parameters used
        print(" Parameters Used:")
        for key, value in api_params.items():
            if key not in ["model", "messages"]:
                print(f"   {key}: {value}")
        
        print(f"\n Prompt: {args.prompt}")
        print(f" Output: {output}")
        
        # Prepare markdown output
        params_str = ", ".join([f"{k}: {v}" for k, v in api_params.items() if k not in ["model", "messages"]])
        md_output = f"### Single Generation\n\n**Parameters:** {params_str}\n\n**Output:**\n{output}\n"
        
        # Save to markdown file
        save_to_md(md_output, "Single Generation", args.prompt, timestamp)
        
        return output
        
    except Exception as e:
        print(f" Error: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(
        description="LLM Parameters CLI Tool - Test OpenAI API parameters",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate.py --prompt "Write a story" --temperature 0.8
  python generate.py --experiment temperature --prompt "Describe Paris"
  python generate.py --top_p 0.9 --frequency_penalty 0.5 --prompt "List ideas"
  python generate.py --json_mode --prompt "Generate user profile in JSON"
  python generate.py --stop "." --max_tokens 50 --prompt "Write a sentence"
        """
    )
    
    # Main arguments
    parser.add_argument("--prompt", "-p", required=True, help="The prompt to send to the LLM")
    
    # Experiment modes
    parser.add_argument("--experiment", "-e", choices=["temperature", "top_p", "penalties"],
                       help="Run a specific experiment (overrides individual parameters)")
    
    # Individual parameters
    parser.add_argument("--temperature", "-t", type=float, 
                       help="Temperature (0.0-2.0). Higher = more creative")
    parser.add_argument("--top_p", type=float,
                       help="Top-p nucleus sampling (0.0-1.0)")
    parser.add_argument("--frequency_penalty", type=float,
                       help="Frequency penalty (0.0-2.0). Reduces repetition")
    parser.add_argument("--presence_penalty", type=float,
                       help="Presence penalty (0.0-2.0). Encourages new topics")
    parser.add_argument("--max_tokens", type=int, default=200,
                       help="Maximum tokens to generate (default: 200)")
    parser.add_argument("--stop", nargs="+",
                       help="Stop sequences (e.g., --stop '.' '!' '?')")
    parser.add_argument("--seed", type=int,
                       help="Seed for reproducible generation")
    parser.add_argument("--json_mode", action="store_true",
                       help="Force JSON output format")
    
    args = parser.parse_args()
    
    # Run experiments or single generation
    if args.experiment == "temperature":
        run_temperature_experiment(args.prompt)
    elif args.experiment == "top_p":
        run_top_p_experiment(args.prompt)
    elif args.experiment == "penalties":
        run_penalties_experiment(args.prompt)
    else:
        generate_single(args)

if __name__ == "__main__":
    main()