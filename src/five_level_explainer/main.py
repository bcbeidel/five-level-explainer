#!/usr/bin/env python
import sys
import warnings
import argparse
import os
# import a function to return the date in YYYY-MM-DD format
from datetime import date

from typing import Optional, Dict, Any

from crewai.flow.flow import Flow, listen, router, or_, start
from pydantic import BaseModel

from five_level_explainer.crews.research_crew.research_crew import ResearchCrew, ResearchReport
from five_level_explainer.crews.writing_crew.writing_crew import WritingCrew, DraftPost
from five_level_explainer.crews.editing_crew.editing_crew import EditingCrew, ReviewedPost

class FiveLevelExplainerFlowState(BaseModel):
    topic: str = None
    date: str = date.today().strftime("%Y-%m-%d")
    research: str = ""
    content: str = ""
    feedback: Optional[str] = None
    is_valid: bool = False
    retry_count: int = 0

class FiveLevelExplainerFlow(Flow[FiveLevelExplainerFlowState]):

    @start()
    def generate_research_report(self):
        print("Conducting Initial Research on topic:", self.state.topic)
        print(self.state)
        
        result = (
            ResearchCrew()
            .crew()
            .kickoff(inputs={"topic": self.state.topic, 'date': self.state.date})
        )

        self.state.research = result.raw
    
    @listen(or_(generate_research_report, 'retry'))
    def generate_five_level_explination(self):
        print("Drafting Post")
        result = (
            WritingCrew()
            .crew()
            .kickoff(inputs={
                "research": self.state.research, 
                "topic": self.state.topic,
                "feedback": self.state.feedback
            })
        )

        self.state.content = result.raw

    @router(generate_five_level_explination)
    def evaluate_explanation(self):
        if self.state.retry_count > 5:
            return "max_retry_exceeded"

        result = EditingCrew().crew().kickoff(inputs={
            "topic": self.state.topic,
            "content": self.state.content, 
            "research_report": self.state.research
        })
        self.state.is_valid = result["is_valid"]
        self.state.feedback = result["feedback"]

        print("valid", self.state.is_valid)
        print("feedback", self.state.feedback)
        self.state.retry_count += 1

        if self.state.is_valid:
            return "complete"

        return "retry"

    @listen("complete")
    def save_result(self):
        print("The post is valid")
        print("Post:", self.state.content)

        # Save the valid X post to a file
        with open("./output/content.md", "w") as file:
            file.write(self.state.content)

    @listen("max_retry_exceeded")
    def max_retry_exceeded_exit(self):
        print("Max retry count exceeded")
        print("X post:", self.state.content)
        print("Feedback:", self.state.feedback)


def kickoff(topic: str = 'Why are Martha Stewart and Ina Garten fighting?'):
    inputs = {'topic': topic}
    FiveLevelExplainerFlow().kickoff(inputs)

def plot():
    FiveLevelExplainerFlow().plot()
    
def check_required_env_vars() -> list[str]:
    required_env_vars = {
        'OPENAI_API_KEY': 'OpenAI API key',
        'SERPER_API_KEY': 'Serper API key'
    }
    
    return [var for var, name in required_env_vars.items() if not os.getenv(var)]

def print_missing_env_vars_message(missing_vars):
    var_descriptions = {
        'OPENAI_API_KEY': 'OpenAI API key',
        'SERPER_API_KEY': 'Serper API key'
    }
    
    message = "Error: Missing required environment variables:\n"
    for var in missing_vars:
        message += f"- {var} ({var_descriptions.get(var, '')})\n"
    
    message += "\nPlease set these environment variables before running the application.\n"
    message += "You can set them by:\n"
    message += "1. Creating a .env file in your project root\n"
    message += "2. Setting them in your shell:\n"
    message += "   export OPENAI_API_KEY=your_key_here\n"
    message += "   export SERPER_API_KEY=your_key_here\n"
    
    print(message, end='')

def main():
    parser = argparse.ArgumentParser(description='Generate a five-level explanation for any topic')
    parser.add_argument('topic', type=str, nargs='?', 
                       default='Why is the sky blue?',
                       help='The topic to explain')
    
    args = parser.parse_args()
    
    # Check environment variables
    missing_vars = check_required_env_vars()
    if missing_vars:
        print_missing_env_vars_message(missing_vars)
        sys.exit(1)
        
    kickoff(args.topic)

if __name__ == "__main__":
    main()
