# main.py
import streamlit as st
from langchain_openai import ChatOpenAI
from crewai import Crew, Process
from dotenv import load_dotenv
import os
from agents import create_agents
from tasks import create_tasks
import re
import requests

# Load environment variables
load_dotenv()


def initialize_llm():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")

    return ChatOpenAI(
        model="gpt-4",  # Changed from "gpt-4o-mini" to "gpt-4"
        temperature=0.7,
        api_key=api_key
    )


def run_market_research(company_name, industry):  # Added industry parameter
    try:
        # Initialize LLM
        llm = initialize_llm()

        # Create agents and tasks
        agents = create_agents(llm)
        tasks = create_tasks(company_name, agents)

        # Create and run crew
        crew = Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential
        )

        result = crew.kickoff()

        # Access individual task results
        industry_research = str(tasks[0].output)
        use_cases = str(tasks[1].output)
        resources = str(tasks[2].output)

        return [industry_research, use_cases, resources]
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None


def generate_report(company_name, results):
    return f"""# AI Analysis Report for {company_name}

## 1. Industry Analysis
{results[0]}

## 2. Recommended AI Use Cases
{results[1]}

## 3. Implementation Resources
{results[2]}

---
This report was generated automatically using the Enterprise AI Use Case Generator.
"""


def verify_link(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False


def save_resource_links(company_name, resources):
    # Extract links using regex
    links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', resources)

    # Prepare the content
    content = f"# Verified Resource Links for {company_name} AI Use Cases\n\n"
    for text, url in links:
        if verify_link(url):
            content += f"- [{text}]({url})\n"
        else:
            content += f"- {text} (Link not verified)\n"

    # Save to file
    filename = f"{company_name}_verified_resources.md"
    with open(filename, "w") as f:
        f.write(content)

    return filename


def main():
    st.set_page_config(
        page_title="AI Use Case Generator",
        layout="wide"
    )

    st.title("🤖 AI Use Case Generator")

    # Add description
    st.markdown("""
    ### Transform your business with AI
    This tool analyzes your company and generates actionable AI use cases backed by industry research and resources.
    """)

    # Company input with additional context
    col1, col2 = st.columns([2, 1])
    with col1:
        company_name = st.text_input(
            "Enter Company Name",
            placeholder="e.g., Tesla, Amazon, etc."
        )
    with col2:
        industry = st.selectbox(
            "Select Industry",
            ["Technology", "Automotive", "Retail",
                "Healthcare", "Financial Services", "Other"]
        )

    if company_name and st.button("Generate AI Use Cases", type="primary"):
        with st.spinner("Analyzing... This may take a few minutes..."):
            results = run_market_research(company_name, industry)

            if results:
                # Industry Research Section
                st.header("🔍 Industry Analysis")
                st.markdown(results[0])

                # AI Use Cases Section
                st.header("💡 Recommended AI Use Cases")
                st.markdown(results[1])

                # Resources Section
                st.header("🔗 Implementation Resources")
                # Changed from results[1] to results[2]
                st.markdown(results[2])

                # Add download buttons
                col1, col2, col3 = st.columns(3)

                with col2:
                    st.download_button(
                        label="📥 Download Full Report",
                        data=generate_report(company_name, results),
                        file_name=f"{company_name}_ai_analysis.md",
                        mime="text/markdown"
                    )


if __name__ == "__main__":
    main()
