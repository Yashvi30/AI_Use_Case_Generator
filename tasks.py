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
        description="""For each identified use case:
        1. Find relevant datasets with direct links
        2. Identify technology stack and tools needed
        3. List implementation resources and tutorials
        4. Include case studies and research papers
        5. Format all links in markdown with brief descriptions""",
        expected_output="A comprehensive resource guide with clickable links in markdown format.",
        agent=agents[2]
    )

    return [industry_research, use_case_generation, resource_collection]
