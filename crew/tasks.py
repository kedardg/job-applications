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
            "Using the semantic_search_resume tool, identify the most relevant sections of the resume at {super_resume_path} that align "
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
        agent=relevance_selector
    )

    emphasis_task = Task(
        description=(
            "Utilize all the data provided by the user and fill in all the data generated in the new resume in the provided "
            "LaTeX template. Replace the placeholders marked with << >> with the appropriate information. "
            "The [[tag]] markers indicate the beginning and end of repeatable sections."
        ),
        expected_output=(
            r"""A LaTeX formatted output which has all the details for the generated resume on the following LaTeX format:
            
            \documentclass[resume]
            \usepackage[implicit=false]{hyperref}
            \usepackage{enumitem}
            \setlist[topsep=-3pt, itemsep=-3pt]
            \usepackage[left=0.45in,top=0.4in,right=0.45in,bottom=0.4in]geometry
            \newcommand\tab[1]\hspace.2667\textwidth\rlap#1
            \newcommand\MYhref[3][blue]\href#2\color#1#3
            \newcommand\itab[1]\hspace0em\rlap#1

            \name\Large <<full_name>>
            \address\href[mailto:<<email>>]<<email>> \\ \href[https://www.linkedin.com/in/<<linkedin_profile>>]www.linkedin.com/in/<<linkedin_profile>> \\ 
            \href[tel:<<phone>>]<<phone>> \\ <<city>>, <<state>>

            \begin[document]

            %----------------------------------------------------------------------------------------
            %	EDUCATION SECTION
            %----------------------------------------------------------------------------------------
            \begin[rSection]Education

            [[education_start]]
            \bf <<degree>>, <<major>> $|$ <<university>> \hfill <<start_date>> - <<end_date>> \\
            \bf Courses:  <<courses>>

            \vspace0.5pt
            [[education_end]]

            \end[rSection]

            %----------------------------------------------------------------------------------------
            % TECHNICAL STRENGTHS	
            %----------------------------------------------------------------------------------------
            \begin[rSection]SKILLS

            \begin[tabular][ @[] >\bfseriesl @\hspace[6ex] l ]
            [[skill_category_start]]
            <<skill_category>> & <<skills>> \\
            [[skill_category_end]]
            \end[tabular]

            \end[rSection]

            %----------------------------------------------------------------------------------------
            %	WORK EXPERIENCE SECTION
            %----------------------------------------------------------------------------------------
            \begin[rSection]EXPERIENCE

            [[job_start]]
            \textbf<<job_title>>, \href[<<company_website>>]<<company_name>> - <<city>>, <<state>> \hfill <<start_date>> - <<end_date>>
            \begin[itemize]
                [[achievement_start]]
                \item <<achievement>>
                [[achievement_end]]
            \end[itemize]

            [[job_end]]

            \end[rSection] 

            \begin[rSection]PROJECTS

            [[project_start]]
            \item \textbf<<project_name>>
                \begin[itemize]
                [[description_start]]
                \item <<description>>
                [[description_end]]
                \end[itemize]

            [[project_end]]

            \end[rSection]

            %----------------------------------------------------------------------------------------
            %	CERTIFICATIONS AND ACHIEVEMENTS SECTION (Optional)
            %----------------------------------------------------------------------------------------
            % \begin[rSection]Certifications and achievements
            % \begin[itemize]
            %     \item Certification or achievement
            %     \item Certification or achievement
            %     \item Certification or achievement
            % \end[itemize]
            % \end[rSection]

            %----------------------------------------------------------------------------------------
            %	LEADERSHIP SECTION (Optional)
            %----------------------------------------------------------------------------------------
            % \begin[rSection]Leadership
            % \begin[itemize]
            %     \item Leadership experience
            %     \item Leadership experience
            %     \item Leadership experience
            % \end[itemize]
            % \end[rSection]

            \end[document]
            """
        ),
        output_file="latex_resume.md",
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
        agent=cover_letter_writer
    )

    return job_analysis_task, relevance_task, emphasis_task, cover_letter_task

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create tasks for job application process")
    parser.add_argument("dummy_arg", help="This script doesn't require arguments when run directly, but needs to be imported")
    args = parser.parse_args()

    print("This script is meant to be imported, not run directly.")