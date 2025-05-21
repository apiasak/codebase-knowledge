# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This repository contains a tool that analyzes GitHub repositories or local codebases and automatically generates beginner-friendly tutorial documentation. It identifies core abstractions, analyzes relationships between them, determines a logical order for presenting concepts, and creates detailed markdown files that explain how the code works.

The system uses a flow-based architecture with PocketFlow to process codebases in steps:
1. Fetch files from GitHub/local directory
2. Identify key abstractions
3. Analyze relationships between abstractions
4. Determine optimal chapter order
5. Generate detailed chapter content for each abstraction
6. Combine everything into a tutorial with visualization

## Command Reference

### Setup and Installation

```bash
# Clone the repository
git clone https://github.com/The-Pocket/PocketFlow-Tutorial-Codebase-Knowledge

# Install dependencies
pip install -r requirements.txt

# Set up LLM API key
# Add your API key to utils/call_llm.py or use environment variables
# By default, Gemini Pro 2.5 is used
export GEMINI_API_KEY="your-api-key"

# Verify LLM setup is working
python utils/call_llm.py
```

### Generating Tutorials

```bash
# Analyze a GitHub repository
python main.py --repo https://github.com/username/repo --include "*.py" "*.js" --exclude "tests/*" --max-size 50000

# Analyze a local directory
python main.py --dir /path/to/your/codebase --include "*.py" --exclude "*test*"

# Generate a tutorial in another language
python main.py --repo https://github.com/username/repo --language "Thai"
```

### Using the Streamlit Web Interface

```bash
# Run the Streamlit app for a GUI interface
streamlit run streamlit_app.py
```

## Core Architecture

The application uses PocketFlow, a 100-line LLM framework, to orchestrate a series of nodes that process the codebase:

1. **FetchRepo** (`nodes.py`): Retrieves files from GitHub or local directory.
2. **IdentifyAbstractions** (`nodes.py`): Uses LLM to identify key abstractions in the codebase.
3. **AnalyzeRelationships** (`nodes.py`): Uses LLM to determine how abstractions relate.
4. **OrderChapters** (`nodes.py`): Determines logical ordering for concepts.
5. **WriteChapters** (`nodes.py`): Generates detailed markdown content for each abstraction.
6. **CombineTutorial** (`nodes.py`): Assembles final output with index and visualization.

The flow connecting these nodes is defined in `flow.py`.

## Key Files

- `main.py`: Entry point that parses arguments and runs the tutorial flow
- `flow.py`: Defines the PocketFlow workflow that coordinates the nodes
- `nodes.py`: Contains all node implementations for the tutorial generation process
- `utils/call_llm.py`: Handles LLM API calls with caching and logging
- `utils/crawl_github_files.py`: Handles fetching files from GitHub repositories
- `utils/crawl_local_files.py`: Handles reading files from local directories
- `streamlit_app.py`: Provides a web interface for the tool

## Development Guidelines

When modifying this codebase:

1. Ensure LLM prompts in nodes are carefully tuned and include proper validation of responses
2. Handle file pattern filtering consistently between GitHub and local sources
3. Support proper translation if working with non-English tutorial generation
4. Maintain the flow-based architecture with well-defined responsibilities in each node
5. Use slugify for filenames to handle special characters in abstraction names
6. Ensure proper context is passed between nodes through the shared data store

## Custom LLM Setup

The system supports multiple LLM backends (Anthropic Claude, OpenAI, Gemini). To use a different LLM:

1. Edit `utils/call_llm.py`
2. Uncomment or add the implementation for your preferred LLM
3. Provide the necessary API keys through environment variables

## Common Issues

- GitHub API rate limiting: Use a GitHub token with `--token` or `GITHUB_TOKEN` env var
- LLM token limits: Large codebases may need filtering with `--include`/`--exclude`
- File encoding: Non-UTF-8 files may cause issues during reading