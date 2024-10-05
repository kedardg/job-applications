import argparse
from crewai import Crew
from crew.agents import create_agents
from crew.tasks import create_tasks
from crew.utils import load_config, print_llm_assignments

def run_job_application_process(resume_path, config_path):
    # Load configuration
    config = load_config(config_path)

    # Create agents
    job_analyzer, relevance_selector, emphasis_strategist, cover_letter_writer = create_agents(resume_path, config)

    # Create tasks
    job_analysis_task, relevance_task, emphasis_task, cover_letter_task = create_tasks(
        job_analyzer, relevance_selector, emphasis_strategist, cover_letter_writer
    )

    # Create and run the crew
    job_application_crew = Crew(
        agents=[job_analyzer, relevance_selector, emphasis_strategist, cover_letter_writer],
        tasks=[job_analysis_task, relevance_task, emphasis_task, cover_letter_task],
        verbose=True
    )

    # Prepare inputs for the crew
    job_application_inputs = {
        'job_posting_url': config.get('job_posting_url', ''),
        'super_resume_path': resume_path,
        'job_description': config.get('job_description', '')
    }

    # Run the crew
    result = job_application_crew.kickoff(inputs=job_application_inputs)
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run job application process")
    parser.add_argument("resume_path", help="Path to the resume file")
    parser.add_argument("config_path", help="Path to the config file")
    args = parser.parse_args()

    print("Starting job application process...")
    print_llm_assignments(load_config(args.config_path))
    
    result = run_job_application_process(args.resume_path, args.config_path)
    
    print("\nJob Application Process Completed")
    print("\nResults:")
    print(result)
