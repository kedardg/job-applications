import json
import os
import re
import subprocess
import tempfile
import markdown
import pdfkit
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

import re

def post_process_latex(content):
    # Remove [[ and ]] tags
    content = re.sub(r'\[\[.*?\]\]', '', content)
    
    # Replace the lines before \name with the provided lines
    replacement_text = r"""\documentclass{resume} % Use the custom resume.cls style
        \usepackage{enumitem}
        \setlist{topsep=-3pt, itemsep=-3pt}
        \usepackage[left=0.45in ,top=0.4in, right=0.45in ,bottom=0.4in]{geometry} % Document margins
        \newcommand{\tab}[1]{\hspace{.2667\textwidth}\rlap{#1}} 
        \newcommand{\MYhref}[3][blue]{\href{#2}{\color{#1}{#3}}}
        \newcommand{\itab}[1]{\hspace{0em}\rlap{#1}}
        """

    content = re.sub(r'^.*?(?=\\name)', replacement_text, content, flags=re.DOTALL)
    
    # Replace [ with { and ] with } for LaTeX commands
    content = re.sub(r'\\(\w+)\[', r'\\\1{', content)
    content = content.replace(']', '}')
    
    return content


def convert_ltx_to_pdf(md_file, cls_file, output_pdf_name="output.pdf"):
    """
    Converts a Markdown file containing LaTeX content within ```latex ``` tags into a PDF.
    Uses a specified LaTeX class (.cls) file.
    
    Args:
    - md_file: Path to the Markdown (.md) file containing LaTeX content inside ```latex ``` tags.
    - cls_file: Path to the .cls file that will be used to format the LaTeX document.
    - output_pdf_name: The name of the output PDF file (default: "output.pdf").
    """
    
    # Step 1: Extract LaTeX content from the Markdown file
    def extract_latex_from_md(md_file):
        """
        Extracts the LaTeX content enclosed within ```latex and ``` tags in the markdown file.
        """
        with open(md_file, 'r') as f:
            content = f.read()

        # Regex to extract content between ```latex and ```
        match = re.search(r"```latex(.*?)```", content, re.DOTALL)
        if match:
            return match.group(1).strip()
        else:
            print("No LaTeX content found in the Markdown file.")
            return None

    # Extract the LaTeX content
    latex_content = extract_latex_from_md(md_file)
    if not latex_content:
        print("Failed to extract LaTeX content. Aborting.")
        return

    # Step 2: Post-process the LaTeX content
    latex_content = post_process_latex(latex_content)

    try:
        # Step 3: Create a temporary directory to store the LaTeX and .cls files
        with tempfile.TemporaryDirectory() as tempdir:
            # Paths for the LaTeX and class file
            latex_file_path = os.path.join(tempdir, "document.tex")
            class_file_name = os.path.basename(cls_file)
            class_file_dest_path = os.path.join(tempdir, class_file_name)

            # Write the post-processed LaTeX content to a temporary .tex file
            with open(latex_file_path, "w") as latex_file:
                latex_file.write(latex_content)

            # Copy the .cls file to the temporary directory
            with open(cls_file, "r") as class_file:
                with open(class_file_dest_path, "w") as dest_file:
                    dest_file.write(class_file.read())

            # Step 4: Compile the LaTeX file using pdflatex
            print("Compiling LaTeX file...")
            subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', '-output-directory', tempdir, latex_file_path],
                check=True
            )

            # Step 5: Move the generated PDF to the current directory
            pdf_file_path = os.path.join(tempdir, "document.pdf")
            if os.path.isfile(pdf_file_path):
                final_output_path = os.path.join(os.getcwd(), output_pdf_name)
                with open(pdf_file_path, "rb") as pdf_file:
                    with open(final_output_path, "wb") as output_pdf_file:
                        output_pdf_file.write(pdf_file.read())
                print(f"PDF generated successfully: {final_output_path}")
            else:
                print("Failed to generate PDF.")

    except subprocess.CalledProcessError as e:
        print(f"Error during LaTeX compilation: {e}")

def convert_md_to_pdf(md_files):
    for md_file in md_files:
        # Check if the file exists
        if not os.path.exists(md_file):
            print(f"The file '{md_file}' does not exist. Skipping...")
            continue
        
        # Generate the PDF file name by replacing the .md extension with .pdf
        pdf_file = os.path.splitext(md_file)[0] + '.pdf'
        
        # Read the Markdown file
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()

        # Convert Markdown to HTML
        html_content = markdown.markdown(md_content)

        # Convert HTML to PDF
        pdfkit.from_string(html_content, pdf_file)

        print(f"Markdown file '{md_file}' has been converted to '{pdf_file}'.")