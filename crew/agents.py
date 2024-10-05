import os
from crewai import Agent
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, FileReadTool, MDXSearchTool
from .utils import get_llm

def create_agents(resume_path, config):
    # Set the Serper API key in the environment
    os.environ["SERPER_API_KEY"] = config['api_keys']['serper']

    # Create tools
    search_tool = SerperDevTool()
    scrape_tool = ScrapeWebsiteTool()
    read_resume = FileReadTool(file_path=resume_path)
    semantic_search_resume = MDXSearchTool(mdx=resume_path)

    agent_llms = config.get('agent_llms', {})
    default_llm = {"service": "openai", "model": "gpt-4"}

    job_analyzer = Agent(
        role="Tech Job Researcher and Analyzer",
        goal="Scrape the job posting URL, extract the job description, and analyze key requirements.",
        tools=[scrape_tool, search_tool],
        verbose=True,
        llm=get_llm(config, agent_llms.get('job_analyzer', default_llm)),
        allow_delegation=True,
        memory=True,
        backstory=(
            "As a Job Researcher, your prowess in "
            "navigating and extracting critical "
            "information from job postings is unmatched. "
            "Your skills help pinpoint the necessary "
            "qualifications and skills sought "
            "by employers, forming the foundation for "
            "effective application tailoring."
        )
    )

    relevance_selector = Agent(
        role="Relevance Selector",
        goal="Identify and justify the most relevant sections in the resume based on the job description analysis.",
        tools=[read_resume, semantic_search_resume, search_tool],
        verbose=True,
        llm=get_llm(config, agent_llms.get('relevance_selector', default_llm)),
        allow_delegation=True,
        memory=True,
        backstory="You excel at matching resume content to job requirements, using semantic search to find the most relevant information."
    )

    emphasis_strategist = Agent(
        role="Latex Resume Strategist",
        goal="Strategically utilize the created resume and rewrite it in latex format for an exemplary resume.",
        tools=[read_resume, semantic_search_resume, search_tool],
        verbose=True,
        llm=get_llm(config, agent_llms.get('emphasis_strategist', default_llm)),
        allow_delegation=True,
        memory=True,
        backstory="Your expertise lies in highlighting key terms that will catch a recruiter's eye and demonstrate the candidate's fit for the role."
    )

    cover_letter_writer = Agent(
        role="Cover Letter Writer",
        goal="Craft a compelling, tailored cover letter that highlights the candidate's qualifications and enthusiasm for the role.",
        tools=[read_resume, semantic_search_resume, search_tool],
        verbose=True,
        llm=get_llm(config, agent_llms.get('cover_letter_writer', default_llm)),
        allow_delegation=False,
        memory=True,
        backstory="You are a master of persuasive writing, able to create cover letters that effectively showcase a candidate's fit for a specific role and company culture."
    )

    return job_analyzer, relevance_selector, emphasis_strategist, cover_letter_writer