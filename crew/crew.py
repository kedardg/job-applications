from crewai import Crew
from agents import job_analyzer, relevance_selector, emphasis_strategist, cover_letter_writer
from tasks import job_analysis_task, relevance_task, emphasis_task, cover_letter_task

# Crew setup
job_application_crew = Crew(
    agents=[job_analyzer, relevance_selector, emphasis_strategist, cover_letter_writer],
    tasks=[job_analysis_task, relevance_task, emphasis_task, cover_letter_task],
    verbose=True
)

# Inputs for the job application process
job_application_inputs = {
    'job_posting_url': 'https://www.linkedin.com/jobs/view/4011986711/?alternateChannel=search&refId=p02ZIOilkaTOINMOOZOPEA%3D%3D&trackingId=xnldLTQp8%2BpuVplwxN6OkQ%3D%3D',
    'super_resume_path': './super_resume.md',
    'job_description': '''
             Stealth
AI Research Scientist [28557]
Cupertino, CA 

About:
We are a Series A startup focused on developing cutting-edge compressed models for devices. Our mission is to bring powerful AI capabilities to edge devices, enabling seamless integration of advanced language models into everyday technology. Join us as we push the boundaries of AI, creating impactful solutions optimized for real-world applications.

Responsibilities:
    Create datasets for potential, powerful capabilities of language models such as function calling and reflection
    Build tooling and infrastructure to enable efficient fine-tuning experiments on language models
    Help develop new methods or novel fine-tuning techniques to improve language model behaviors
    Run experiments that feed into key AI research

You may be a good fit if you:
    Have at least 1 research project related to machine learning in which you played a major role
    Significant Python, machine learning, research experience
    Are results-oriented, with a bias towards urgency, impact, and flexibility
    Be familiar with C or C++
        '''
}

# Execute the job application process
result = job_application_crew.kickoff(inputs=job_application_inputs)

print("\nJob Application Package:")
print(result)
