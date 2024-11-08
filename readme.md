# AI Use Case Generator

## Overview

The AI Use Case Generator is a multi-agent system that analyzes companies and generates tailored AI implementation recommendations. It uses CrewAI framework to orchestrate multiple AI agents that work together to provide comprehensive analysis and actionable insights.
![alt text](docs\images\image.png)

## Features

- Industry and company analysis
- AI use case generation
- Resource and dataset recommendations
- Interactive web interface
- Exportable reports

## Architecture

![Architecture Flowchart](docs/images/architecture_flowchart.png)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Yashvi30/AI_Use_Case_Generator.git
cd ai-use-case-generator
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment variables:

```bash
python -m venv venv
#Create .env with your API keys
```

4. Run the application:

```bash
streamlit run main.py
```

## Usage

1. Enter company name
2. Select industry
3. Click "Generate AI Use Cases"
4. Review analysis and download reports

## Documentation

- [Architecture Details](docs/architecture.md)
- [Methodology](docs/methodology.md)
