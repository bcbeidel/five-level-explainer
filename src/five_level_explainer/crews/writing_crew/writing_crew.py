from pydantic import BaseModel

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class WritingCrew():
	"""writing crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def lead_writer(self) -> Agent:
		return Agent(
			config=self.agents_config['lead_writer'],
			verbose=False,
			llm='gpt-4o-mini'
		)
	
	@agent
	def childrens_writer(self) -> Agent:
		return Agent(
			config=self.agents_config['childrens_writer'],
			verbose=False,
			llm='gpt-4o-mini'
		)
	
	@agent
	def teen_writer(self) -> Agent:
		return Agent(
			config=self.agents_config['teen_writer'],
			verbose=False,
			llm='gpt-4o-mini'
		)
	
	@agent
	def college_writer(self) -> Agent:
		return Agent(
			config=self.agents_config['college_writer'],
			verbose=False,
			llm='gpt-4o-mini'
		)

	@agent
	def college_writer(self) -> Agent:
		return Agent(
			config=self.agents_config['college_writer'],
			verbose=False,
			llm='gpt-4o-mini'
		)

	@agent
	def graduate_writer(self) -> Agent:
		return Agent(
			config=self.agents_config['graduate_writer'],
			verbose=False,
			llm='gpt-4o-mini'
		)

	@agent
	def postgrad_writer(self) -> Agent:
		return Agent(
			config=self.agents_config['postgrad_writer'],
			verbose=False,
			llm='gpt-4o-mini'
		)
	
	@task
	def draft_childrens_content_task(self) -> Task:
		return Task(
			config=self.tasks_config['draft_childrens_content_task'],
		)

	@task
	def draft_teen_content_task(self) -> Task:
		return Task(
			config=self.tasks_config['draft_teen_content_task'],
		)
	
	@task
	def draft_undergrad_content_task(self) -> Task:
		return Task(
			config=self.tasks_config['draft_undergrad_content_task'],
		)
	
	@task
	def draft_graduate_content_task(self) -> Task:
		return Task(
			config=self.tasks_config['draft_graduate_content_task'],
		)
	
	@task
	def draft_postgrad_content_task(self) -> Task:
		return Task(
			config=self.tasks_config['draft_postgrad_content_task'],
		)

	@task
	def combine_draft_content_task(self) -> Task:
		return Task(
			config=self.tasks_config['combine_draft_content_task'],
			context=[
				self.draft_childrens_content_task(),
				self.draft_teen_content_task(),
				self.draft_undergrad_content_task(),
				self.draft_graduate_content_task(),
				self.draft_postgrad_content_task(),
			]
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Writing crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			verbose=True,
			process=Process.sequential, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
    		planning=True
		)
