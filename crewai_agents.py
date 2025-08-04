import warnings
warnings.filterwarnings('ignore')
import os

from crewai import Agent, Task, Crew, LLM
from crewai_tools import WebsiteSearchTool
from dotenv import load_dotenv

load_dotenv()

my_llm = LLM(
              model='gemini/gemini-2.0-flash',
              api_key=os.environ["GOOGLE_API_KEY"]
            )

history_search = WebsiteSearchTool(
    config=dict(
        llm=dict(
            provider="google", 
            config=dict(
                model="gemini-2.0-flash",
                # temperature=0.5,
                # top_p=1,
                # stream=true,
            ),
        ),
        embedder=dict(
            provider="google", # or openai, ollama, ...
            config=dict(
                model="models/embedding-001",
                task_type="retrieval_document",
                # title="Embeddings",
            ),
        ),
    ),
    search_params={
        'time': 'y',
        'region':'wt-wt',
        'safesearch':'off',
        'max_results': 5
    }
)

archivist = Agent(
    role='Primary Sources Archivist',
    goal='Locate authentic historical documents and primary sources on {topic}',
    backstory=(
        "You are an expert archivist with many years of experience under your belt"
        "You specialize mainly in affairs concerning the history of Uganda particularly after independence and only look for sources concerning that."
        "You are skilled in verifying authenticity of sources." 
        
    ),
    llm=my_llm,
    verbose=True,
    allow_delegation=False
    
)

historian = Agent(
    role='Historical Analyst',
    goal='Interpret historical events and identify patterns',
    backstory=(
        "A history professor with expertise in historical causation and comparative analysis. "
        "You critically evaluate sources and identify historical significance."
        "You are are keen on detail and have a knack for connecting the dots between events and their broader implications."
        "Your main area of focus is the history of Uganda after independence."
    ),
    llm=my_llm,
    verbose=True,
    allow_delegation=True
)

storyteller = Agent(
    role='Historical Narrator',
    goal='Create engaging historical narratives',
    backstory=(
        "An historical novelist who transforms complex events into compelling stories "
        "while maintaining academic rigor and factual accuracy."
    ),
    llm=my_llm,
    verbose=True
)

source_task = Task(
    description=(
        "Investigate primary sources about {topic} between {start_year} and {end_year}. "
        "Locate documents, eyewitness accounts, and contemporary records. "
        "Verify authenticity and provenance of sources."
    ),
    expected_output=(
        "Annotated bibliography with:\n"
        "- 5-10 verified primary sources\n"
        "- Source origin and context\n"
        "- Reliability assessment\n"
        "- Key insights from each source"
    ),
    agent=archivist,
    tools=[history_search]
)

analysis_task = Task(
    description=(
        "Analyze the historical significance of {topic}. "
        "Examine causes, key figures, societal impact, and long-term consequences. "
        "Compare with similar historical patterns. Identify scholarly debates."
    ),
    expected_output=(
        "Academic report with:\n"
        "- Chronological analysis\n"
        "- Key turning points\n"
        "- Historiographical context\n"
        "- 3+ scholarly interpretations\n"
        "- Modern relevance"
    ),
    agent=historian,
    context=[source_task],
)

narrative_task = Task(
    description=(
        "Create an engaging historical narrative about {topic} for {audience} audience. "
        "Incorporate human perspectives while maintaining factual accuracy. "
        "Highlight dramatic moments and personal stories."
        "Properly bring out the causes and effects of the events in the narrative."
    ),
    expected_output=(
        "A 3-part narrative in Markdown format:\n"
        "1. Setting the stage (context)\n"
        "2. The unfolding events (dramatic arc)\n"
        "3. Legacy and lessons (impact)\n"
        "With vivid historical details and quotes"
    ),
    agent=storyteller,
    context=[analysis_task],
    output_file='historical_narrative.md'
)

history_crew = Crew(
    agents=[archivist, historian, storyteller],
    tasks=[source_task, analysis_task, narrative_task],
    verbose=True,
    #memory=True
)

result = history_crew.kickoff(inputs={
    'topic': 'Post-independence Uganda',
    'start_year': '1962',
    'end_year': '1985',
    'audience': 'high school students'
})

