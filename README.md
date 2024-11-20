# file_levels_explainer

A bot that explains arbitrary things at 5 levels.  An experiment with [CrewAI](https://docs.crewai.com/).

- Level 1: Can you explain it to a child?
- Level 2: Can you explain it to a teenager?
- Level 3: Can you explain it to an undergrad?
- Level 4: Can you explain it to a grad student?
- Level 5: Can you explain it to a college, an expert scientist?

Explinations are put into a fixed file in the `output` directory.

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
