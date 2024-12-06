from typing import Optional

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from pydantic import BaseModel
from crewai_tools import (
    SerperDevTool,
    WebsiteSearchTool,
)

class ReviewedPost(BaseModel):
	is_valid: bool
	feedback: Optional[str]

@CrewBase
class EditingCrew():
	"""editing crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def editor(self) -> Agent:
		return Agent(
			config=self.agents_config['editor'],
			tools=[
				SerperDevTool(),
				WebsiteSearchTool()
			],
			verbose=False,
			llm='gpt-4o-mini'
		)

	@task
	def editing_task(self) -> Task:
		return Task(
			config=self.tasks_config['editing_task'],
			output_pydantic=ReviewedPost
		)
	

	@crew
	def crew(self) -> Crew:
		"""Creates the editing crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
