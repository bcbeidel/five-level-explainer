from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
	CodeDocsSearchTool,
	DirectoryReadTool,
	FileReadTool,
	FileWriterTool,
    SerperDevTool,
	YoutubeVideoSearchTool, 
	YoutubeChannelSearchTool, 
)

@CrewBase
class ResearchCrew():
	"""Research Crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# exclude the @agent decorator from the research manager pass it as the manager_agent
	def research_manager(self) -> Agent:
		return Agent(
			config=self.agents_config['research_manager'],
			verbose=False,
			llm='gpt-4o-mini'
		)

	@agent
	def web_and_document_researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['web_and_document_researcher'],
			verbose=False,
			tools=[
				SerperDevTool(), 
				CodeDocsSearchTool()
			],
			llm='gpt-4o-mini'
		)
	
	@agent
	def code_researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['code_researcher'],
			verbose=False,
			tools=[
				CodeDocsSearchTool(),
				SerperDevTool(),
			],
			llm='gpt-4o-mini'
		)

	@agent
	def video_researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['video_researcher'],
			verbose=False,
			tools=[
				SerperDevTool(),
				YoutubeVideoSearchTool(), 
				YoutubeChannelSearchTool(), 
			],
			llm='gpt-4o-mini'
		)
	
	@agent
	def fact_checker(self) -> Agent:
		return Agent(
			config=self.agents_config['fact_checker'],
			tools=[
				CodeDocsSearchTool(),
				SerperDevTool(),
				YoutubeVideoSearchTool(), 
				YoutubeChannelSearchTool(), 
			],
			verbose=False,
			llm='gpt-4o-mini'
		)

	@task
	def research_topic_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_topic_task']
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Research crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.hierarchical,
			verbose=True,
			manager_agent=self.research_manager(),
			long_term_memory = None,
            short_term_memory=None,
            entity_memory=None
		)
