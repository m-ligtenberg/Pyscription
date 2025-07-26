# Pyscription 💊

**Medication for your Python headaches**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code Quality](https://img.shields.io/badge/code%20quality-A-green.svg)](https://github.com/m-ligtenberg/pyscription)

===============================

Pyscription is an AI‑enhanced command‑line assistant designed to help you
maintain, refactor and analyze Python code. Although it operates like a
doctor reviewing a patient file – diagnosing patterns, prescribing fixes
and guiding your workflow – this document adopts a more conventional tone
for clarity and ease of use.

Key qualities:

* **Production ready** – suited for real projects and active codebases.
* **Security first** – includes multiple vulnerability checks.
* **AI powered** – uses locally hosted language models for intelligent
  suggestions.
* **Privacy conscious** – all analysis happens on your machine.

## Overview

Pyscription learns from your coding patterns and provides context‑aware
suggestions, much like a seasoned software physician might review a
patient’s history and offer treatment. It includes several modes of
operation, each tailored to a different aspect of development:

* **Conversational mode** – chat with the Doctor about Python topics and
  code snippets, receiving explanations and advice.
* **Autonomous surgeon mode** – let the Surgeon analyze your entire
  codebase, build an improvement plan and apply changes automatically.
* **Security analysis** – scan for common vulnerabilities and code
  weaknesses in accordance with standards like CWE and OWASP.
* **Pattern discovery** – detect design patterns and code smells using
  machine learning.
* **Documentation search** – perform semantic searches through Python
  documentation to retrieve relevant information.

## Getting Started

### Prerequisites

* Python 3.8 or higher.
* [Ollama](https://ollama.ai/) for local language model support (optional,
  fallback mode available, but as of now very limited).

### Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/m-ligtenberg/pyscription.git
cd pyscription
pip install -r requirements.txt
````

Run the setup command to download documentation and prepare the
environment:

```bash
python3 -m pyscription --setup
```

### Usage

Pyscription can be invoked through the terminal;

```
python3 -m pyscription [options] [file]

Options:
  --pill             Apply a mild correction (lint, style, syntax).
  --inject           Perform targeted code changes.
  --overdose         Apply all available fixes without prompts.
  --refill           Repeat the previous operation.
  --side-effects     Display a list of recent changes.
  --interactive      Start a conversational session with the AI Doctor.
  --agent            Run autonomous codebase improvement (Surgeon mode).
  --analyze <file>   Perform static analysis on a single file.
  --search <term>    Semantic search in Python documentation.
  --setup            Initialize the environment and documentation.
```

Examples:

```bash
# Start a chat session with the Doctor
python3 -m pyscription --doctor

# Launch the autonomous Surgeon to improve a project
python3 -m pyscription --surgeon

# Analyze a single file for issues
python3 -m pyscription --analyze your_file.py

# Search the Python documentation
python3 -m pyscription --search "decorator pattern"
```

## Modes in Detail

### Doctor Mode

In doctor mode (`--doctor`), Pyscription becomes a Doctor.
It accepts natural language queries and code snippets and returns
detailed answers and suggestions. Use this mode to ask about language
features, design patterns or the structure of a given function. The
interface displays syntax‑highlighted code and ensures the dialogue
remains focused.

### Surgeon Mode

The surgeon mode (`--surgeon`), allows Pyscription to perform a comprehensive analysis of your codebase, plan
refactors and apply changes. This mode is similar to handing over your
patient chart to a trusted surgeon: the system reviews the code,
identifies areas for improvement and executes tasks while maintaining
backups. You can specify the number of tasks or time allotted to the
Surgeon for each session.

### Security Analysis

Pyscription includes built‑in security checks that detect common
vulnerabilities such as SQL injection, command injection, hardcoded
credentials and path traversal. It maps issues to the Common Weakness
Enumeration (CWE) standards and can help you move toward OWASP
compliance. Use the analysis options (`--analyze`) or engage the
Surgeon mode for a broader review.

### Pattern Discovery

Machine‑learning modules examine your code to find recurring design
patterns and code smells. Detected patterns include Singleton, Factory
and Observer. When a pattern is identified, Pyscription will suggest
improvements or templates. This feature helps maintain architecture
consistency across large projects.

**DISCLAIMER:** The model is still being trained, so it is still very unoptimized as of now.

### Documentation Intelligence

Pyscription can search the Python documentation semantically, providing
context‑aware suggestions during development. If you need to recall how
a particular standard library module works or want examples of a design
pattern, use the `--search` option or ask directly in conversational
mode.

## Architecture

The project is organized into modules corresponding to its major
functions:

```
pyscription/
├── core/                     # Core machine learning components
│   ├── doctor_interactive.py # Orchestrates high‑level operations (Doctor)
│   ├── document_processor.py # Documentation analysis logic
│   ├── pattern_discovery.py  # Pattern detection algorithms
│   ├── local_ai.py           # Local model integration
│   ├── autonomous_surgeon.py # Autonomous Surgeon implementation
│   ├── project_analyzer.py   # Project‑wide static analysis
│   └── security_analyzer.py  # Security scanning utilities
├── cli/                      # Command‑line interface modules
│   ├── doctor.py             # Handles conversational sessions
│   └── surgeon.py            # Handles agent sessions
├── utils/                    # Miscellaneous utilities
│   ├── terminal_styling.py   # Terminal UI helpers
│   └── documentation_downloader.py # Doc download and indexing
└── __main__.py               # Entry point
```

## Terminal UI

Pyscription provides an intuitive terminal interface with a clear colour
scheme, clear syntax highlighting and responsive animations. During
analysis and refactoring tasks you can monitor progress through
dashboards and status messages. The design seeks to minimize fatigue and
help you focus on the content of your work.

## Privacy and Security

All analysis and model inference take place on your machine; Pyscription
sends no telemetry or code externally. You can operate entirely offline
once the necessary models and documentation are downloaded. Internal
security measures ensure that code execution during analysis does not
affect your system.

## Performance

Pyscription is optimized for real‑time feedback. Startup times are
typically under two seconds, memory usage remains modest (around
200 MB for most sessions) and the system scales to projects with over
100 k lines of code. Performance may vary depending on the complexity of
the repository and the machine’s resources.

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for
details on how to report issues, propose features or submit pull
requests. When contributing, please maintain the project’s overall tone
and ensure that the program continues to behave like a careful
software physician.

### Development Setup

```bash
git clone https://github.com/m-ligtenberg/pyscription.git
cd pyscription
pip install -r requirements-dev.txt
python -m pytest tests/      # Run tests
flake8 pyscription/          # Check style
```

## License

Pyscription is released under the MIT License. Refer to the
[LICENSE](LICENSE) file for the full terms.

## Acknowledgments

We extend our thanks to the Ollama team for providing the local language
model infrastructure and to the Python community for their extensive
documentation. Without these foundations, Pyscription could not serve as
an effective development assistant.

## Support

For bug reports, discussions and feature requests please use the
appropriate channels on GitHub:

* [Issues](https://github.com/m-ligtenberg/pyscription/issues)
* [Discussions](https://github.com/m-ligtenberg/pyscription/discussions)
* [Wiki](https://github.com/m-ligtenberg/pyscription/wiki)

If you have questions about the tool or need guidance on its usage, feel
free to open a discussion thread.
