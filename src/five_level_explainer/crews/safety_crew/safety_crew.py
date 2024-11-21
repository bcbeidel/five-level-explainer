from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from pydantic import BaseModel

class SafetyEvaluation(BaseModel):
    is_safe: bool
    reason: str
    votes_for_safety: int
    votes_against_safety: int

@CrewBase
class SafetyCrew():
	"""Safety Crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def safety_officer(self) -> Agent:
		return Agent(
			config=self.agents_config['safety_officer'],
			verbose=False,
			llm='gpt-4o-mini'
		)

	@task
	def evaluate_topic_safety_task(self) -> Task:
		return Task(
			config=self.tasks_config['evaluate_topic_safety_task'],
			output_pydantic=SafetyEvaluation,
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Safety crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=False,
		)
