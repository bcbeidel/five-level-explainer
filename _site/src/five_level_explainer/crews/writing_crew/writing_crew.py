from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class WritingCrew():
	"""Writing crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def writer(self) -> Agent:
		return Agent(
			config=self.agents_config['writer'],
			verbose=False,
			llm='gpt-4o-mini'
		)

	@task
	def draft_content_task(self) -> Task:
		return Task(
			config=self.tasks_config['draft_explanation_task']
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Writing crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
		)