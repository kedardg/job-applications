# Job Applications Enhancement Tool

Welcome to the **Job Applications Enhancement Tool** repository. This tool utilizes various agentic technologies to help users optimize their job applications by suggesting improvements based on the job description.

## Features

- **Resume Analysis:** Compares your comprehensive resume with the job description to highlight the most relevant points.
- **Document Generation:** Automatically generates a cover letter, optimized resume, and a file suggesting sections to emphasize in your application.

## Getting Started

Follow these steps to set up and use the tool:

### Prerequisites

- **OpenAI API Account:** You need an OpenAI API key to use certain features of this tool.
  - Create an account and add credits by following the instructions here: [OpenAI Production Best Practices](https://platform.openai.com/docs/guides/production-best-practices/api-keys).

- **Serper Account:** This tool uses Serper for web scraping and search functionalities.
  - Sign up at [Serper.dev](https://serper.dev) to get free 2000 queries.

### Prepare Your Resume

1. **Create a Super Resume:** Ensure your resume includes all details about your professional history.
2. **Convert Your Resume to Markdown:**
   - If your resume is in PDF format, convert it using [PDF to Markdown](https://pdf2md.morethan.io/).
   - If your resume is in LaTeX format, convert it using [Pandoc](https://pandoc.org/try/).
3. **Add the Converted Resume:** Name the file `resume.md` and add it to the project folder.

### Usage

1. **Enter Your API Keys:** When you run the notebook, you will be prompted to enter your OpenAI and Serper API keys.
2. **Execute the Notebook:** Run the notebook to generate your documents.
3. **Output:** The results will be generated as both PDF and Markdown files, including a cover letter, an optimized resume, and suggestions for possible sections to highlight in your application.

## Contributing

Contributions to this project are welcome! Please feel free to fork the repository, make changes, and submit a pull request.

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## Contact

If you have any questions or suggestions, please feel free to reach out by creating an issue in this repository.

Thank you for using the Job Applications Enhancement Tool!
