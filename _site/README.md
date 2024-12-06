# file-level-explainer

https://bcbeidel.github.io/five-level-explainer/

---

This is a toy project using [CrewAI](https://www.crewai.com/). Inspired by Wired's [5-Levels](https://www.wired.com/video/series/5-levels), where any topic from the user is turned into a 5-level explainer progressing from a child's reading level up to to an expert scientist.

- Level 1: Can you explain it to a child?
- Level 2: Can you explain it to a teenager?
- Level 3: Can you explain it to an undergrad?
- Level 4: Can you explain it to a grad student?
- Level 5: Can you explain it to an expert scientist?

Explinations are put into a fixed file in the `docs` directory and hosted via a [Jekyll](https://jekyllrb.com/) static site with [GitHub pages](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll) here [https://bcbeidel.github.io/five-level-explainer/](https://bcbeidel.github.io/five-level-explainer/).

## Local Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/bcbeidel/file_levels_explainer.git
   cd file_levels_explainer
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install the package in development mode:
   ```bash
   pip install -e .
   ```

4. Set up required API keys:
   Create a `.env` file in the project root with the following content:
   ```
   OPENAI_API_KEY=your_openai_key_here
   SERPER_API_KEY=your_serper_key_here
   ```
   
   Or set them directly in your environment:
   ```bash
   export OPENAI_API_KEY=your_openai_key_here
   export SERPER_API_KEY=your_serper_key_here
   ```

   You can obtain these API keys from:
   - OpenAI API key: https://platform.openai.com/api-keys
   - Serper API key: https://serper.dev/api-key

## Running the Project

Once installed, you can run the explainer using:

```bash
explain 'topic you want explained'
```

## Things To Try

- Include monitoring with [Langtrace Monitoring](https://docs.crewai.com/how-to/langtrace-observability)
- Experiment with [Task Planning](https://docs.crewai.com/concepts/planning)
- Experiment with [hierarchical processes](https://docs.crewai.com/how-to/hierarchical-process)
- Use tools to check for previous answers ([directory read](https://docs.crewai.com/tools/directoryreadtool) vs [directory RAG](https://docs.crewai.com/tools/directorysearchtool) vs. [text search](https://docs.crewai.com/tools/txtsearchtool))
- If a question has been answered, re-route to the existing file ([Conditional Tasks](https://docs.crewai.com/how-to/conditional-tasks))
- Interrupt flow for [user input](https://docs.crewai.com/how-to/human-input-on-execution)


User Stories
- A user can request for an explanation of a topic (through a command line interface)
- A user can view an explanation (in markdown format)
- A user can view MLA citations for all referenced source materials
- A user can view a copy of all referenced source material (in a local directory)

## Intended Flow

1. Safety Crew: 
   - Evaluates user requests determines if it is safe to respond, or if the rest of the flow should be abandonede. 
   - Use a single agent with a [Tree of Thoughts](https://www.promptingguide.ai/techniques/tot) prompt to encourage safe responses.
2. Customer Service Crew: 
   - Reviews previous answers to see if the question has already been answered. If so, re-route to the existing file. 
   - Will need to use a [Directory Read](https://docs.crewai.com/tools/directoryreadtool) tool, a [File Read](https://docs.crewai.com/tools/filereadtool) Tool, to re-route, leveraging a [Few-Shot](https://www.promptingguide.ai/techniques/fewshot) prompting technique to provide examples of how to re-route. 
3. Research Crew: 
   - Identifies, collects, and summarizes primary sources. Additionally, it will download any relevant content, and store it in a local directory.  
   - Will need to leverage a litany of tools to download pdfs, website content, or youtube videos and transcripts or other media.
   - Will leverage a [hierarchical process](https://docs.crewai.com/how-to/hierarchical-process) to conduct research allowing the managing agent to freely delgate to other agents.
4. Writing Crew: 
   - Writes an explanation of the topic at 5 levels of complexity.
5. Review Crew:
   - Reads the explanation and ensures it is accurate and helpful.
   - If the explanation is not helpful, or accurate the flow should be re-routed back to the research crew to improve the explanation.
6. Publishing Crew:
   - Publishes the explanation to a user.
   - Writes to a file in the output directory.
