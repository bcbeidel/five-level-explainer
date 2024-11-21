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
from colorama import Fore, Style

from five_level_explainer.crews.safety_crew.safety_crew import SafetyCrew
from five_level_explainer.crews.research_crew.research_crew import ResearchCrew
from five_level_explainer.crews.writing_crew.writing_crew import WritingCrew
from five_level_explainer.crews.editing_crew.editing_crew import EditingCrew
from five_level_explainer.crews.publish_crew.publish_crew import PublishCrew

class FiveLevelExplainerFlowState(BaseModel):
    topic: str = 'Why is the sky blue?'
    date: str = date.today().strftime("%Y-%m-%d")
    research_report: str = ""
    content: str = ""
    feedback: Optional[str] = None
    is_valid: bool = False
    retry_count: int = 0
    file_name: str = ""
    is_safe: bool = False
    reason: str = ""
    votes_for_safety: int = 0
    votes_against_safety: int = 0

class FiveLevelExplainerFlow(Flow[FiveLevelExplainerFlowState]):

    def color_print(self, text: str, color: str) -> None:
        """Print text in specified color using colorama.
        
        Args:
            text (str): The text to print
            color (str): Color from colorama.Fore (e.g., 'BLUE', 'RED', 'GREEN')
        """
        color_code = getattr(Fore, color.upper(), Fore.WHITE)  # Default to white if color not found
        print(f"{color_code}{text}{Style.RESET_ALL}")

    @start()
    def evaluate_topic_safety(self):
        """Evaluates the topic safety, if the topic is not safe, the flow will exit."""

        self.color_print(text="Evaluating topic safety...", color="BLUE")
        
        result = SafetyCrew().crew().kickoff(inputs={"topic": self.state.topic})
        self.state.is_safe = result['is_safe']
        self.state.reason = result['reason']
        self.state.votes_for_safety = result['votes_for_safety']
        self.state.votes_against_safety = result['votes_against_safety']
        
    @router(evaluate_topic_safety)
    def evaluate_topic_safety_router(self):
        """Evaluates the topic safety, if the topic is not safe, the flow will exit."""

        if not self.state.is_safe:
            self.color_print(f"We are sorry, but we are unable to explain this topic. {self.state.reason}", "RED")
            return None # exits from the flow

        return "conduct_research"

    @listen("conduct_research")
    def generate_research_report(self):
        """Generates a research report on the topic."""

        self.color_print(text="Conducting Research...", color="BLUE")
            
        result = (
            ResearchCrew()
            .crew()
            .kickoff(inputs={"topic": self.state.topic, 'date': self.state.date})
        )

        self.state.research_report = result.raw
    
    @listen(or_(generate_research_report, 'retry'))
    def generate_five_level_explination(self):
        print("Drafting Post")
        result = (
            WritingCrew()
            .crew()
            .kickoff(inputs={
                "research_report": self.state.research_report,
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
            "research_report": self.state.research_report
        })

        self.state.is_valid = result["is_valid"]
        self.state.feedback = result["feedback"]
        self.state.retry_count += 1
        
        if self.state.is_valid:
            return "publish"

        return "retry"
    
    @listen("publish")
    def generate_file_name(self):
        result = PublishCrew().crew().kickoff(inputs={
            "topic": self.state.topic,
            "content": self.state.content, 
            "date": self.state.date
        })

        self.state.file_name = result['file_name']

    @listen("generate_file_name")
    def save_result(self):
        print("The post is valid")
        print("Post:", self.state.content)

        # Save the valid X post to a file
        with open(f"./output/{self.state.file_name}", "w") as file:
            file.write(self.state.content)

    @listen("max_retry_exceeded")
    def max_retry_exceeded_exit(self):
        print("Max retry count exceeded")
        print("Content:", self.state.content)
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
                       default=FiveLevelExplainerFlowState().topic,
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
