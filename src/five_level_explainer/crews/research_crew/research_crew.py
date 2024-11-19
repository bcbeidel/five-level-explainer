from typing import Optional

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from pydantic import BaseModel
from crewai_tools import (
    SerperDevTool,
    WebsiteSearchTool,
)

class ResearchReport(BaseModel):
    content: str
    key_terms: str

@CrewBase
class ResearchCrew():
	"""Research Crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			verbose=False,
			tools=[SerperDevTool(), WebsiteSearchTool()],
			llm='gpt-4o-mini'
		)

	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
			output_pydantic=ResearchReport,
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Research crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
		)
