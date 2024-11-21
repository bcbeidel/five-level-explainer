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

from five_level_explainer.utils.env_checker import color_print, check_required_env_vars, print_missing_env_vars_message

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

    @start()
    def evaluate_safety_of_topic(self):
        """Evaluates the topic safety, if the topic is not safe, the flow will exit."""

        color_print(text="Evaluating topic safety...", color="BLUE")
        
        result = SafetyCrew().crew().kickoff(inputs={"topic": self.state.topic})
        self.state.is_safe = result['is_safe']
        self.state.reason = result['reason']
        self.state.votes_for_safety = result['votes_for_safety']
        self.state.votes_against_safety = result['votes_against_safety']
        
    @router(evaluate_safety_of_topic)
    def respond_to_safety_decision(self):
        """Evaluates the topic safety, if the topic is not safe, the flow will exit."""

        if not self.state.is_safe:
            color_print(f"We are sorry, but we are unable to explain this topic. {self.state.reason}", "RED")
            return "exit_flow" # exits from the flow

        return "start_research"

    @listen("start_research")
    def conduct_research(self):
        """Generates a research report on the topic."""

        color_print(text="Conducting Research...", color="BLUE")
            
        result = (
            ResearchCrew()
            .crew()
            .kickoff(inputs={"topic": self.state.topic, 'date': self.state.date})
        )

        self.state.research_report = result.raw
    
    @listen('conduct_research')
    @listen('retry')
    def write_explanation(self):
        """Generates a five-level explanation for the topic."""

        color_print(text="Drafting explanation...", color="BLUE")

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

    @router(write_explanation)
    def edit_explanation(self):
        """Evaluates the final post, if the post is not valid, the flow will retry."""

        color_print(text="Editing explanation...", color="BLUE")

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
    def finalize_explanation(self):
        """Generates a file name for the final post."""

        color_print(text="Finalizing explanation...", color="BLUE")

        result = PublishCrew().crew().kickoff(inputs={
            "topic": self.state.topic,
            "content": self.state.content, 
            "date": self.state.date
        })

        self.state.file_name = result['file_name']

    @listen("generate_file_name")
    def save_explanation(self):
        """Publishes the final post."""

        color_print(text="Saving explanation...", color="BLUE")

        # Save the valid X post to a file
        with open(f"./output/{self.state.file_name}", "w") as file:
            file.write(self.state.content)
        return "exit_flow"

    @listen("max_retry_exceeded")
    def max_retry_exceeded_exit(self):
        print("Max retry count exceeded")
        print("Content:", self.state.content)
        print("Feedback:", self.state.feedback)
        return "exit_flow"

    @listen("exit_flow")
    def exit(self):
        color_print("Exiting flow...", "BLUE")


def kickoff(topic: str = 'Why are Martha Stewart and Ina Garten fighting?'):
    inputs = {'topic': topic}
    FiveLevelExplainerFlow().kickoff(inputs)

def plot():
    FiveLevelExplainerFlow().plot()

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
