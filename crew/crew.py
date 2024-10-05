import argparse
from crewai import Crew
from agents import create_agents
from tasks import create_tasks

def run_job_application_process(job_posting_url, resume_path, job_description):
    job_analyzer, relevance_selector, emphasis_strategist, cover_letter_writer = create_agents(resume_path)
    job_analysis_task, relevance_task, emphasis_task, cover_letter_task = create_tasks(job_analyzer, relevance_selector, emphasis_strategist, cover_letter_writer)

    job_application_crew = Crew(
        agents=[job_analyzer, relevance_selector, emphasis_strategist, cover_letter_writer],
        tasks=[job_analysis_task, relevance_task, emphasis_task, cover_letter_task],
        verbose=True
    )

    job_application_inputs = {
        'job_posting_url': job_posting_url,
        'super_resume_path': resume_path,
        'job_description': job_description
    }

    result = job_application_crew.kickoff(inputs=job_application_inputs)
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run job application process")
    parser.add_argument("job_posting_url", help="URL of the job posting")
    parser.add_argument("resume_path", help="Path to the resume file")
    parser.add_argument("job_description", help="Job description text")
    args = parser.parse_args()

    result = run_job_application_process(args.job_posting_url, args.resume_path, args.job_description)
    print("\nJob Application Package:")
    print(result)