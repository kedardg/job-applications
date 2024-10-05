# Job Applications Enhancement Tool

Welcome to the **Job Applications Enhancement Tool** repository. This tool leverages CrewAI and various language models to help users optimize their job applications by suggesting improvements based on the job description.

## Features

- **Job Analysis:** Analyzes the job posting to extract key requirements and qualifications.
- **Resume Optimization:** Compares your comprehensive resume with the job description to highlight the most relevant points.
- **Emphasis Strategy:** Suggests words or phrases to emphasize in your resume to catch a recruiter's attention.
- **Cover Letter Generation:** Automatically generates a tailored cover letter based on your resume and the job description.

## Getting Started

Follow these steps to set up and use the tool:

### Prerequisites

- Python 3.8 or higher
- Jupyter Notebook

### API Keys

You need API keys for the following services:

- **OpenAI API:** Used for certain language model tasks.
  - Create an account and add credits [here](https://platform.openai.com/signup).
- **Anthropic API:** Used for Claude language model tasks.
  - Sign up for Anthropic's API [here](https://www.anthropic.com/).
- **Google AI API:** Used for Gemini language model tasks.
  - Get started with Google AI Studio [here](https://makersuite.google.com/app/apikey).
- **Serper API:** Used for web scraping and search functionalities.
  - Sign up at [Serper.dev](https://serper.dev) to get free 2000 queries.

### LaTeX Distribution (New Requirement)

For PDF generation, you'll need a LaTeX distribution installed on your system:

On Linux:
* Install TeX Live:
  ```
  sudo apt-get install texlive-full
  ```

On macOS:
* Install MacTeX from the [MacTeX website](https://www.tug.org/mactex/).

On Windows:
* Install MiKTeX from the [MiKTeX website](https://miktex.org/download) or TeX Live.

Ensure that LaTeX executables (like `pdflatex`) are in your system's `PATH`.

### Optional: Latexmk

For advanced document handling, you may want to install Latexmk:

- It's included in most LaTeX distributions like TeX Live or MacTeX.
- On macOS, if not included, you can install via Homebrew:
  ```
  brew install latexmk
  ```

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/job-applications-enhancement-tool.git
   cd job-applications-enhancement-tool
   ```
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

### Prepare Your Resume

1. **Create a Super Resume:** Ensure your resume includes all details about your professional history.
2. **Convert Your Resume to Markdown:**
   - If your resume is in PDF format, convert it using [PDF to Markdown](https://pdf2md.morethan.io/).
   - If your resume is in LaTeX format, convert it using [Pandoc](https://pandoc.org/try/).
3. **Add the Converted Resume:** Name the file `resume.md` and add it to the project folder.

### Configuration

1. Copy the `config.json.example` file to `config.json`.
2. Add your API keys to the `config.json` file:
   ```json
   {
     "api_keys": {
       "openai": "your_openai_api_key",
       "anthropic": "your_anthropic_api_key",
       "google": "your_google_api_key",
       "serper": "your_serper_api_key"
     },
     ...
   }
   ```

### Usage

1. Open the `Job_Application_Client.ipynb` notebook in Jupyter.
2. Follow the instructions in the notebook to:
   - Specify the path to your resume and config file.
   - Enter the job posting URL and optional job description.
   - Run the job application process.
3. **Output:** The tool will generate the following files:
   - `focused_resume.md`: An optimized version of your resume.
   - `emphasize_strategy.md`: Suggestions for words or phrases to emphasize.
   - `cover_letter.md`: A tailored cover letter for the job.

## Project Structure

```
/
├── job_application_client.py
├── config.json
├── Job_Application_Client.ipynb
├── requirements.txt
├── README.md
└── crew/
    ├── __init__.py
    ├── agents.py
    ├── tasks.py
    └── utils.py
```

## Contributing

Contributions to this project are welcome! Please feel free to fork the repository, make changes, and submit a pull request.

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## Contact

If you have any questions or suggestions, please feel free to reach out by creating an issue in this repository.