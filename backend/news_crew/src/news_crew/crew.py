# from crewai import Agent, Crew, Process, Task
# from crewai.project import CrewBase, agent, crew, task
# from crewai.agents.agent_builder.base_agent import BaseAgent
# from typing import List
# from crewai_tools import SerperDevTool
# from news_crew.tools.gnews_top_headlines_tool import GNewsTopHeadlinesTool
# from crewai_tools import ScrapeWebsiteTool
# from crewai_tools import SpiderTool
# from crewai_tools import HyperbrowserLoadTool

# # Initialize Serper news search tool
# news_search_tool = SerperDevTool(type="news")
# scrape_tool = HyperbrowserLoadTool(
#     api_key="hb_a0082f6b4485ff0233409f73f88d"
# )  # Or use environment variable


# @CrewBase
# class NewsCrew:
#     """NewsCrew crew"""

#     agents: List[BaseAgent]
#     tasks: List[Task]

#     # --- Agents ---
#     @agent
#     def fetcher_agent(self) -> Agent:
#         return Agent(
#             config=self.agents_config["fetcher_agent"],  # from agents.yaml
#             tools=[GNewsTopHeadlinesTool()],
#             verbose=True,
#             memory=True,
#         )

#     @agent
#     def cleaner_agent(self) -> Agent:
#         return Agent(
#             config=self.agents_config["cleaner_agent"],  # from agents.yaml
#             verbose=True,
#         )

#     @agent
#     def summarizer_agent(self) -> Agent:
#         return Agent(
#             config=self.agents_config["summarizer_agent"],
#             tools=[scrape_tool],  # Use HyperbrowserLoadTool
#             verbose=True,
#         )

#     # @agent
#     # def summarizer_agent(self) -> Agent:
#     #     return Agent(
#     #         config=self.agents_config["summarizer_agent"],  # from agents.yaml
#     #         tools=[ScrapeWebsiteTool()],
#     #         verbose=True,
#     #     )

#     # --- Tasks ---
#     @task
#     def fetcher_agent_task(self) -> Task:
#         return Task(
#             config=self.tasks_config["fetcher_agent_task"],  # from tasks.yaml
#         )

#     @task
#     def cleaner_agent_task(self) -> Task:
#         return Task(
#             config=self.tasks_config["cleaner_agent_task"],  # from tasks.yaml
#             output_file="clean_articles.md",  # save clean results
#         )

#     @task
#     def summarizer_agent_task(self) -> Task:
#         return Task(
#             config=self.tasks_config["summarizer_agent_task"],  # from tasks.yaml
#             output_file="summarized_articles.md",  # save summaries
#         )

#     # --- Crew ---
#     @crew
#     def crew(self) -> Crew:
#         """Creates the NewsCrew crew"""
#         return Crew(
#             agents=self.agents,  # auto-collected from @agent decorators
#             tasks=self.tasks,  # auto-collected from @task decorators
#             process=Process.sequential,  # run fetcher → cleaner → summarizer
#             verbose=True,
#         )
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_tools import SerperDevTool
from news_crew.tools.gnews_top_headlines_tool import GNewsTopHeadlinesTool
from crewai_tools import HyperbrowserLoadTool
from news_crew.tools.local_vader_tool import VaderSentimentTool
from crewai.utilities.paths import db_storage_path
from news_crew.tools.ollama_embeddings import OllamaEmbeddings
from crewai.knowledge.knowledge import Knowledge
import os
from pathlib import Path

storage_dir = Path(__file__).parent / "crewai_storage"
os.environ["CREWAI_STORAGE_DIR"] = str(storage_dir)

# Initialize Serper news search tool
news_search_tool = SerperDevTool(type="news")

# Initialize scrapers
hyperbrowser_tool = HyperbrowserLoadTool(
    api_key="hb_a0082f6b4485ff0233409f73f88d"  # Or use env variable
)


@CrewBase
class NewsCrew:
    """NewsCrew crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # sentiment_llm = LLM(
    #     provider="ollama",  # <- Important
    #     model="ollama/mvkvl/sentiments:gemma",  # model name
    #     base_url="http://localhost:11434",  # Ollama server URL
    #     # optionally temperature, etc.
    # )
    # sentiment_llm = LLM(
    #     provider="ollama",
    #     model="mvkvl/sentiments:gemma",  # no "ollama/" prefix
    #     base_url="http://localhost:11434",
    #     temperature=0.1,
    #     max_tokens=800,  # helps avoid truncation
    # )

    # --- Agents ---
    @agent
    def fetcher_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["fetcher_agent"],  # from agents.yaml
            tools=[GNewsTopHeadlinesTool()],
            verbose=True,
            memory=False,
        )

    @agent
    def cleaner_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["cleaner_agent"],  # from agents.yaml
            verbose=True,
            memory=False,
        )

    @agent
    def summarizer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["summarizer_agent"],
            tools=[hyperbrowser_tool],  # single unified tool
            verbose=True,
            memory=True,
        )

    @agent
    def sentiment_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["sentiment_agent"],
            tools=[VaderSentimentTool()],
            verbose=True,
            memory=False,
        )

    @agent
    def knowledge_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["knowledge_agent"],
            verbose=True,
            memory=True,  # ✅ Turn on memory
        )

    # --- Tasks ---
    @task
    def fetcher_agent_task(self) -> Task:
        return Task(
            config=self.tasks_config["fetcher_agent_task"],  # from tasks.yaml
        )

    @task
    def cleaner_agent_task(self) -> Task:
        return Task(
            config=self.tasks_config["cleaner_agent_task"],  # from tasks.yaml
            output_file="clean_articles.json",
        )

    @task
    def summarizer_agent_task(self) -> Task:
        return Task(
            config=self.tasks_config["summarizer_agent_task"],  # from tasks.yaml
            output_file="summarized_articles.json",  # JSON summaries
        )

    @task
    def sentiment_agent_task(self) -> Task:
        return Task(
            config=self.tasks_config["sentiment_agent_task"],
            output_file="sentiment_articles.json",
        )

    @task
    def knowledge_agent_task(self) -> Task:
        return Task(
            config=self.tasks_config["knowledge_agent_task"],
            output_file="knowledge_store.json",
        )

    # # --- Crew ---
    # @crew
    # def crew(self) -> Crew:
    #     """Creates the NewsCrew crew"""
    #     return Crew(
    #         agents=self.agents,  # auto-collected from @agent decorators
    #         tasks=self.tasks,  # auto-collected from @task decorators
    #         process=Process.sequential,  # fetcher → cleaner → summarizer
    #         verbose=True,
    #     )

    @crew
    def crew(self) -> Crew:
        """Creates the NewsCrew crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            memory=True,  # ✅ Enable CrewAI’s memory system
            embedder={
                "provider": "ollama",  # Use local Ollama
                "config": {
                    "model": "mxbai-embed-large",  # You already pulled this
                    "url": "http://localhost:11434/api/embeddings",
                },
            },
        )
