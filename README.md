# Open API Codegen by AI

> An AI-driven procedure that replaces traditional CodeGen tools for generating REST API client libraries.

**Author:** Artur Ziółkowski
**LinkedIn:** [https://www.linkedin.com/in/arturjadach/](https://www.linkedin.com/in/arturjadach/)

---

## 💡 Idea

**Open API Codegen by AI** replaces tools like `swagger-codegen` or `openapi-generator` with an AI-guided, interactive procedure. Instead of generating code from rigid templates, the AI walks the user step by step through gathering requirements and then creates a client library fully tailored to their needs.

---

## ✨ Features

- 🤖 **AI-guided setup** — no config files, no CLI flags; just answer questions
- 📦 **Resource-based grouping** — methods are organized by API resource (e.g. `client.pets.get_all()`, `client.orders.create(...)`)
- 🔁 **Session resume** — progress is saved in `status.json`; the procedure can be interrupted and resumed at any time without losing answers
- 🐍 **Python support** — uses **Pydantic** for argument validation
- 📄 **pip package generation** — optionally builds a `.whl` / `.tar.gz` package ready for distribution
- 🚀 **TestPyPI upload** — optionally publishes the package to TestPyPI

---

## 📋 Prerequisites

- An AI assistant that accepts a system/instruction prompt (e.g. GitHub Copilot, ChatGPT, Claude, etc.)
- A valid OpenAPI 3.x / Swagger 2.x `openapi.json` file for your target API
- Python (if generating a Python library)

---

## � Installation

### From PyPI

```bash
pip install openapi-codegen-agent
```

### From GitHub (latest main branch)

```bash
pip install git+https://github.com/arturjadach/openapi-codegen-agent.git
```

### From a specific tag / branch

```bash
pip install git+https://github.com/arturjadach/openapi-codegen-agent.git@v1.0.0
```

### From local source (editable)

```bash
git clone https://github.com/arturjadach/openapi-codegen-agent.git
cd openapi-codegen-agent
pip install -e .
```

---

## 🖥️ CLI Usage

After installation the `openapi-codegen-agent` command is available in your terminal.

### `install` — add the agent prompt

Copies the bundled `.agent.md` prompt file to the correct location so your AI assistant can use it.

**Default (VS Code User prompts folder):**

```bash
openapi-codegen-agent install
```

The agent file is installed to the VS Code global User prompts directory:

| OS | Path |
|----|------|
| Windows | `%APPDATA%\Code\User\prompts\` |
| macOS | `~/Library/Application Support/Code/User/prompts/` |
| Linux | `~/.config/Code/User/prompts/` |

**Into a test repository (`.github/agents/`):**

```bash
openapi-codegen-agent install --test_repository_path /path/to/your/repo
```

This places the agent file at `<repo>/.github/agents/open-api-code-gen.agent.md`, making it available as a GitHub Copilot agent scoped to that repository. No manual file copying required.

#### `install` parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--test_repository_path DIR` | Path to the target repository. Agent is written to `DIR/.github/agents/`. | VS Code User prompts folder |

You can also set the path via an environment variable instead of the flag:

```bash
# PowerShell
$env:TEST_REPOSITORY_PATH = "C:\Projects\my-api-tests"
openapi-codegen-agent install

# Bash / zsh
export TEST_REPOSITORY_PATH=/projects/my-api-tests
openapi-codegen-agent install
```

---

### `path` — print the bundled agent file path

```bash
openapi-codegen-agent path
```

Prints the absolute path to the `.agent.md` file bundled inside the installed package. Useful for piping or scripting.

---

## 🚀 How to Use

1. **Install the agent prompt** by running `openapi-codegen-agent install` (or `openapi-codegen-agent install --test_repository_path <repo>`).
2. **Open GitHub Copilot** (or another compatible AI assistant) and select the `open-api-code-gen` agent.
3. **Start a conversation.** The AI will:
   - Introduce the library assumptions
   - Guide you through 6 structured steps (see below)
   - Save your answers to `status.json` after each question
4. **Resume any time.** If you close the session, start the agent again — the AI will read `status.json` and continue from where you left off.

---

## 🗂️ Procedure Steps

| Step | Name | Description |
|------|------|-------------|
| 1 | **API Information** | Provide the Swagger URL and base REST API endpoint |
| 2 | **Project Structure** | Name the library folder; place `openapi.json` inside it |
| 3 | **Technical Configuration** | Choose language, version, HTTP library, client folder name, and method prefix style |
| 4 | **Library Generation** | AI reads `openapi.json`, lists modules (tags), and generates the client code |
| 5 | **pip Package** *(Python only)* | Optionally build a pip-installable package and publish to TestPyPI |
| 6 | **Success Summary** | Final report of everything that was generated |

---

## 📁 Generated Project Structure

```
{library_folder}/
├── swagger/
│   └── openapi.json          # Your OpenAPI spec (placed manually)
├── trash_AI/                 # Temporary AI working files (can be ignored)
├── {client_folder}/
│   ├── client.py             # Main client — instantiates all modules
│   └── modules/
│       ├── __init__.py       # Exports all module classes
│       ├── {module_1}.py
│       ├── {module_2}.py
│       └── ...
├── pyproject.toml            # (Python) pip package metadata
└── README.md                 # (Python) auto-generated library README
```

---

## 🔄 Session State (`status.json`)

All collected answers are stored in `status.json` in the working directory:

```json
{
  "swagger_url": null,
  "base_endpoint": null,
  "library_folder": null,
  "openapi_json_confirmed": null,
  "language": null,
  "language_version": null,
  "http_library": null,
  "client_folder": null,
  "method_prefix": null,
  "modules": null,
  "generation": null,
  "pip_package": null,
  "testpypi_upload": null
}
```

The AI skips any question whose field is already non-null, ensuring no answer is collected twice.

---

## 📐 Library Design Principles

- **Resource-based grouping** — API resources map to classes; methods map to endpoints
- **2xx-only contract** — the library assumes success; error handling belongs in tests
- **Test-oriented** — the library is an interface for API testing, not a production SDK
- **Ordered methods** — method order in each class mirrors the endpoint order in `openapi.json`
- **Full docstrings** — every class and method includes a docstring with `description`, `Args:`, and `Returns:` sections sourced from the OpenAPI `summary` field

---

## 🐍 Python-specific Notes

- **Pydantic** is used for argument validation in all generated methods
- A `pyproject.toml` is generated for pip packaging
- The library can also be used locally without installing via pip:

```python
import sys
sys.path.insert(0, "/path/to/{library_folder}")

from {client_folder}.client import <ClientClass>
client = <ClientClass>()
```

---

## 📄 License

MIT
