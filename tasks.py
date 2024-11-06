# tasks.py
from crewai import Task


def create_tasks(company_name, agents):
    industry_research = Task(
        description=f"""Research {company_name} and its industry thoroughly:
        1. Industry segment and market size
        2. Key offerings and revenue streams
        3. Strategic focus areas and growth initiatives
        4. Market position and competitive landscape
        5. Current technology stack and digital maturity
        
        Include references to credible sources (McKinsey, Deloitte, industry reports).""",
        expected_output="A comprehensive report with industry analysis and cited sources.",
        agent=agents[0]
    )

    use_case_generation = Task(
        description=f"""Based on the industry research for {company_name}, generate detailed AI/ML use cases:
        1. Analyze industry-specific AI trends and adoption patterns
        2. Propose 3-5 high-impact AI/ML solutions with:
           - Problem statement
           - Proposed solution
           - Expected benefits
           - Implementation complexity
           - ROI estimation
        3. Include references to similar successful implementations
        4. Prioritize use cases based on business value and feasibility""",
        expected_output="A structured analysis of AI use cases with implementation details and references.",
        agent=agents[1]
    )

    resource_collection = Task(
        description=f"""For each identified AI use case for {company_name}:
        1. Find and provide links to real, existing datasets on Kaggle, HuggingFace, or UCI Machine Learning Repository.
        2. Search for and link to actual research papers on arXiv or IEEE Xplore.
        3. Identify and link to official documentation or tutorials for relevant AI/ML libraries or frameworks.
        4. Find and link to real-world case studies or implementation examples from reputable sources.
        5. Ensure all links are working and directly accessible.
        6. Format each link as: [Brief Description](URL)
        
        Verify each link before including it in your response.""",
        expected_output="A list of verified, working links to real resources for each use case, formatted in markdown.",
        agent=agents[2]
    )

    return [industry_research, use_case_generation, resource_collection]
