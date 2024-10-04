import json
import os
import re
import subprocess
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

def load_config(config_path):
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    
    # Set environment variables if keys are available
    api_keys = config.get('api_keys', {})
    for key, value in api_keys.items():
        env_var_name = f"{key.upper()}_API_KEY"
        if value and env_var_name not in os.environ:
            os.environ[env_var_name] = value
            print(f"Set {env_var_name} environment variable")
    
    return config

def get_llm(config, llm_config):
    service = llm_config['service']
    model = llm_config['model']

    if service == 'openai':
        return ChatOpenAI(
            model=model,
            temperature=0.7,
        )
    elif service == 'anthropic':
        return ChatAnthropic(
            model=model,
            temperature=0.7,
        )
    elif service == 'google':
        return ChatGoogleGenerativeAI(
            model=model,
            temperature=0.7,
        )
    else:
        raise ValueError(f"Unsupported LLM service: {service}")

def print_llm_assignments(config):
    print("LLM assignments:")
    for agent, llm_config in config['agent_llms'].items():
        print(f"{agent.replace('_', ' ').title()}: {llm_config['service']} - {llm_config['model']}")

def post_process_latex(input_file, output_file):
    with open(input_file, 'r') as f:
        content = f.read()
    
    # Replace [[ and ]] with nothing (remove tags)
    content = re.sub(r'\[\[.*?\]\]', '', content)
    
    # Replace [ with { and ] with } for LaTeX commands
    content = re.sub(r'\\(\w+)\[', r'\\\1{', content)
    content = re.sub(r'\]', '}', content)
    
    with open(output_file, 'w') as f:
        f.write(content)

def compile_latex_to_pdf(latex_file, output_file):
    try:
        subprocess.run(['pdflatex', '-output-directory', '.', latex_file], check=True)
        print(f"PDF generated: {output_file}")
    except subprocess.CalledProcessError:
        print("Error: Failed to compile LaTeX to PDF")