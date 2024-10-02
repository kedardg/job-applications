import argparse
from crewai import Task

def create_tasks(job_analyzer, relevance_selector, emphasis_strategist, cover_letter_writer):
    job_analysis_task = Task(
        description=(
            "Analyze the job posting URL provided ({job_posting_url}) "
            "to extract key skills, experiences, and qualifications "
            "required. If you cannot scrape the job description or no relevant information is available from the URL, use ({job_description}) which is an alternative but unstructured version of the job posting. Use the tools to gather content and identify "
            "and categorize the requirements."
        ),
        expected_output=(
            "A structured list of job requirements, including necessary "
            "skills, qualifications, and experiences."
        ),
        agent=job_analyzer
    )

    relevance_task = Task(
        description=(
            "Using the semantic_search_resume tool, identify the most relevant sections of the super resume that align "
            "with the job analysis. Provide a thorough justification for each selected section, explaining how it "
            "demonstrates the candidate's fit for the role. Use the semantic search to find not just keyword matches, "
            "but conceptually relevant experiences and skills."
        ),
        expected_output=(
            "A shortened resume tailored to the job requirements. Stay true to the original resume and do not hallucinate. Follow the existing resume format and keep the following on the focused resume:\n"
            "1. The list of skills focused towards the job description but a few more from the existing list to show the breadth of skills by following the section's original format\n"
            "2. A minimum of 4 jobs under work experience and a total of 10 bullet points\n"
            "3. A minimum of 2 and maximum of 3 projects with the same bullet points with possible minor improvements.\n"
            "4. Make changes to potential areas where the section could be enhanced to better match the job description\n"
            "5. Bold all keywords which will help a recruiter quickly analyze the created resume\n"
            "6. A brief explanation of key decisions made in crafting the resume, including:\n"
            "   - Choice of highlighted experiences and skills\n"
            "   - How the resume addresses specific job requirements\n"
            "   - Any company-specific references or customizations\n"
            "   - Any other customizations"
        ),
        output_file="focused_resume.md",
        agent=relevance_selector,
        context=[job_analysis_task]
    )

    emphasis_task = Task(
        description=(
            "Analyze the selected relevant sections and the job requirements to identify key words or phrases that should "
            "be bolded to enhance the resume's impact. Use the semantic_search_resume tool to identify terms that are "
            "conceptually important, not just exact matches. For each suggestion, provide a clear rationale explaining its "
            "significance in relation to the job requirements and how it will catch the attention of recruiters or ATS systems."
        ),
        expected_output=(
            "A comprehensive list of words/phrases to be bolded, organized by resume section. For each suggestion, include:\n"
            "1. The word or phrase to be bolded\n"
            "2. The resume section it appears in\n"
            "3. A detailed explanation of why this term is crucial, referencing specific job requirements\n"
            "4. If applicable, suggest minor rewording to better align the term with the job description language\n"
            "5. The semantic search query used to identify this term (if applicable)\n"
            "6. Strategically bold phrases/words to avoid the recruiter only reading in the F shaped pattern and end up avoiding any critical information"
        ),
        output_file="emphasize_strategy.md",
        agent=emphasis_strategist,
        context=[job_analysis_task, relevance_task]
    )

    cover_letter_task = Task(
        description=(
            "Using the job analysis and resume optimization insights, craft a compelling cover letter that highlights "
            "the candidate's qualifications and enthusiasm for the role. Tailor the letter to the specific job and company."
        ),
        expected_output=(
            "A well-structured, tailored cover letter that includes:\n"
            "1. An engaging opening paragraph that captures attention and states the purpose\n"
            "2. 2-3 body paragraphs that highlight the candidate's most relevant qualifications, using specific examples from the resume\n"
            "3. A closing paragraph that reiterates interest and suggests next steps\n"
            "4. Appropriate tone and style for the industry and company culture\n"
            "5. A brief explanation of key decisions made in crafting the letter, including:\n"
            "   - Choice of highlighted experiences and skills\n"
            "   - How the letter addresses specific job requirements\n"
            "   - Any company-specific references or customizations"
        ),
        output_file="cover_letter.md",
        agent=cover_letter_writer,
        context=[job_analysis_task, relevance_task]
    )

    return job_analysis_task, relevance_task, emphasis_task, cover_letter_task

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create tasks for job application process")
    parser.add_argument("dummy_arg", help="This script doesn't require arguments when run directly, but needs to be imported")
    args = parser.parse_args()

    print("This script is meant to be imported, not run directly.")