from typing import Optional

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from pydantic import BaseModel

class FileDetails(BaseModel):
    file_name: str

@CrewBase
class PublishCrew():
	"""Publish Crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def publisher(self) -> Agent:
		return Agent(
			config=self.agents_config['publisher'],
			verbose=False,
			tools=[],
			llm='gpt-4o-mini'
		)

	@task
	def finish_post_task(self) -> Task:
		return Task(
			config=self.tasks_config['finish_post_task'],
			output_pydantic=FileDetails,
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Publish crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
		)
