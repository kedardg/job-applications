import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

def load_config(config_path):
    with open(config_path, 'r') as config_file:
        return json.load(config_file)

def get_llm(config, llm_config):
    api_keys = config['api_keys']
    service = llm_config['service']
    model = llm_config['model']

    if service == 'openai':
        return ChatOpenAI(
            model=model,
            temperature=0.7,
            api_key=api_keys['openai']
        )
    elif service == 'anthropic':
        return ChatAnthropic(
            model=model,
            temperature=0.7,
            api_key=api_keys['anthropic']
        )
    elif service == 'google':
        return ChatGoogleGenerativeAI(
            model=model,
            temperature=0.7,
            google_api_key=api_keys['google']
        )
    else:
        raise ValueError(f"Unsupported LLM service: {service}")

def print_llm_assignments(config):
    print("LLM assignments:")
    for agent, llm_config in config['agent_llms'].items():
        print(f"{agent.replace('_', ' ').title()}: {llm_config['service']} - {llm_config['model']}")
