# main.py
import streamlit as st
from langchain_openai import ChatOpenAI
from crewai import Crew, Process
from dotenv import load_dotenv
import os
from agents import create_agents
from tasks import create_tasks

# Load environment variables
load_dotenv()


def initialize_llm():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")

    return ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=api_key
    )


def run_market_research(company_name):
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


# main.py
def main():
    st.set_page_config(
        page_title="Enterprise AI Use Case Generator",
        layout="wide"
    )

    st.title("🤖 Enterprise AI Use Case Generator")

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
            ["Technology", "Automotive", "Retail", "Healthcare", "Financial Services", "Other"]
        )

    if company_name and st.button("Generate AI Use Cases", type="primary"):
        with st.spinner("Analyzing... This may take a few minutes..."):
            results = run_market_research(company_name)

            if results:
                # Industry Research Section
                st.header("🔍 Industry Analysis")
                st.markdown(results[0])
                
                # AI Use Cases Section
                st.header("💡 Recommended AI Use Cases")
                st.markdown(results[1])
                
                # Resources Section
                st.header("🔗 Implementation Resources")
                st.markdown(results[2])

                # Export options
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        label="📥 Download Full Report",
                        data=generate_report(company_name, results),
                        file_name=f"{company_name}_ai_analysis.md",
                        mime="text/markdown"
                    )
                with col2:
                    st.download_button(
                        label="📊 Download Executive Summary",
                        data=generate_executive_summary(company_name, results),
                        file_name=f"{company_name}_executive_summary.md",
                        mime="text/markdown")
    st.set_page_config(
        page_title="AI Use Case Generator",
        layout="wide"
    )

    st.title("AI Use Case Generator")

    # Add description
    st.markdown("""
    This app analyzes companies and generates AI use cases using CrewAI and GPT.
    Enter a company name below to get started.
    """)

    # Company input
    company_name = st.text_input(
        "Enter Company Name",
        placeholder="e.g., Tesla"
    )

    if company_name and st.button("Generate Use Cases"):
        with st.spinner("Analyzing... This may take a few minutes..."):
            results = run_market_research(company_name)

            if results:
                # Display results in expandable sections
                with st.expander("Industry Research", expanded=True):
                    st.markdown(results[0])

                with st.expander("AI Use Cases", expanded=True):
                    st.markdown(results[1])

                with st.expander("Resources", expanded=True):
                    st.markdown(results[2])

                # Add download button for results
                st.download_button(
                    label="Download Results",
                    data=f"""# Analysis Results for {company_name}

## Industry Research
{results[0]}

## AI Use Cases
{results[1]}

## Resources
{results[2]}
""",
                    file_name=f"{company_name}_analysis.md",
                    mime="text/markdown"
                )


if __name__ == "__main__":
    main()
