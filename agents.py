# agents.py
from langchain_openai import ChatOpenAI
from crewai import Agent
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper


def create_agents(llm):
    # Initialize tools
    search_tool = DuckDuckGoSearchRun()
    wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

    industry_researcher = Agent(
        role='Industry Research Analyst',
        goal='Conduct thorough industry and company research',
        verbose=True,
        memory=True,
        backstory="""You are an experienced industry analyst with expertise in 
        understanding market trends and company positioning.""",
        tools=[search_tool, wikipedia],
        llm=llm,
        allow_delegation=True
    )

    use_case_analyst = Agent(
        role='AI Use Case Specialist',
        goal='Generate relevant AI/ML use cases based on research',
        verbose=True,
        memory=True,
        backstory="""You are an AI/ML solutions architect with deep knowledge of 
        implementing AI solutions across industries.""",
        tools=[search_tool],
        llm=llm,
        allow_delegation=False
    )

    resource_collector = Agent(
        role='Resource Asset Collector',
        goal='Find and collect relevant datasets and resources',
        verbose=True,
        memory=True,
        backstory="""You are a data specialist skilled at finding relevant datasets 
        and resources.""",
        tools=[search_tool],
        llm=llm,
        allow_delegation=False
    )

    return [industry_researcher, use_case_analyst, resource_collector]
