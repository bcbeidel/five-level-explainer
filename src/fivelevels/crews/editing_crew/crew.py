from typing import Optional

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from pydantic import BaseModel
from crewai_tools import (
    DirectoryReadTool,
    FileReadTool,
    SerperDevTool,
    WebsiteSearchTool,
	FileWriterTool,
	TXTSearchTool,
)



class ReviwedPost(BaseModel):
    valid: bool
    feedback: Optional[str]

@CrewBase
class fiveLevelsCrew():
	"""fivelevels crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			verbose=True,
			tools=[
				SerperDevTool(), 
				WebsiteSearchTool(), 
				FileWriterTool(directory='./temp', overwrite=True),
				DirectoryReadTool('./temp'),
			],
			llm='gpt-4o-mini'
		)

	@agent
	def education_writer(self) -> Agent:
		return Agent(
			config=self.agents_config['education_writer'],
			verbose=True,
			tools=[
				DirectoryReadTool('./temp'),
				FileWriterTool(directory='./temp', overwrite=True),
			],
			llm='gpt-4o-mini'
		)

	@agent
	def fact_checker(self) -> Agent:
		return Agent(
			config=self.agents_config['fact_checker'],
			tools=[
				SerperDevTool(),
				WebsiteSearchTool(), 
				FileWriterTool(directory='./temp', overwrite=True),
				FileReadTool(research_path),
				FileReadTool(draft_path),
			],
			verbose=True,
			llm='gpt-4o-mini'
		)

	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
		)

	@task
	def draft_post_task(self) -> Task:
		return Task(
			config=self.tasks_config['draft_post_task'],
			context=[self.research_task()],
		)
	
	@task
	def fact_check_task(self) -> Task:
		return Task(
			config=self.tasks_config['fact_check_task'],
			context=[self.research_task(), self.draft_post_task()],
		)
	
	@task
	def finalize_post_task(self) -> Task:
		return Task(
			config=self.tasks_config['finalize_post_task'],
			expected_output=final_path
		)	

	@crew
	def crew(self) -> Crew:
		"""Creates the Eli5 crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
