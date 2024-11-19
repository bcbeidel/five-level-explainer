#!/usr/bin/env python
import sys
import warnings
# import a function to return the date in YYYY-MM-DD format
from datetime import date

from typing import Optional

from crewai.flow.flow import Flow, listen, router, or_, start
from pydantic import BaseModel

from five_level_explainer.crews.research_crew.research_crew import ResearchCrew, ResearchReport
from five_level_explainer.crews.writing_crew.writing_crew import WritingCrew, DraftPost
from five_level_explainer.crews.editing_crew.editing_crew import EditingCrew, ReviewedPost

class FiveLevelExplainerFlowState(BaseModel):
    topic: str = ""
    research: str = ""
    content: str = ""
    feedback: Optional[str] = None
    is_valid: bool = False
    retry_count: int = 0

class FiveLevelExplainerFlow(Flow[FiveLevelExplainerFlowState]):

    @start()
    def generate_research_report(self):
        print("Conducting Initial Research")
        
        # Set the initial topic
        self.state.topic = "Why are Martha Steward and Ina Garten fighting?"
        
        result = (
            ResearchCrew()
            .crew()
            .kickoff(inputs={"topic": self.state.topic, 'date': date.today().strftime("%Y-%m-%d")})
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


def kickoff():
    five_level_flow = FiveLevelExplainerFlow()
    five_level_flow.kickoff()


def plot():
    five_level_flow = FiveLevelExplainerFlow()
    five_level_flow.plot()


if __name__ == "__main__":
    kickoff()
