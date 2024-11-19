#!/usr/bin/env python
import sys
import warnings
# import a function to return the date in YYYY-MM-DD format
from datetime import date

from typing import Optional

from crewai.flow.flow import Flow, listen, router, start
from pydantic import BaseModel

from fivelevels.crews.research_crew.research_crew import ResearchCrew, ResearchReport
from fivelevels.crews.writing_crew.writing_crew import WritingCrew, DraftPost
from fivelevels.crews.editing_crew.editing_crew import EditingCrew, ReviewedPost

class FivelevelsPostFlowState(BaseModel):
    topic: str = ""
    research: str = ""
    content: str = ""
    feedback: Optional[str] = None
    is_valid: bool = False
    retry_count: int = 0

class FivelevelsPostFlow(Flow[FivelevelsPostFlowState]):

    @start()
    def generate_research_report(self):
        print("Conducting Initial Research")
        
        # Set the initial topic
        self.state.topic = "Why are Drake and Kendrick Lamar Fighting?"
        
        result = (
            ResearchCrew()
            .crew()
            .kickoff(inputs={"topic": self.state.topic, 'date': date.today().strftime("%Y-%m-%d")})
        )

        print("Research Report Generated: ", result.raw)
        self.state.research = result.raw
        

    @start('retry')
    @listen('generate_research_report')
    def generate_fivelevels_post(self):
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

        print("Draft dontent generated", result.raw)
        self.state.content = result.raw

    @router(generate_fivelevels_post)
    def evaluate_post(self):
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
        with open("content.md", "w") as file:
            file.write(self.state.content)

    @listen("max_retry_exceeded")
    def max_retry_exceeded_exit(self):
        print("Max retry count exceeded")
        print("X post:", self.state.content)
        print("Feedback:", self.state.feedback)


def kickoff():
    fivelevelsflow = FivelevelsPostFlow()
    fivelevelsflow.kickoff()


def plot():
    fivelevelsflow = FivelevelsPostFlow()
    fivelevelsflow.plot()


if __name__ == "__main__":
    kickoff()
