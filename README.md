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

## 🚀 How to Use

1. **Copy the prompt** from [`codgen_prompt.md`](./codgen_prompt.md) and paste it into your AI assistant as the system/instruction prompt.
2. **Start a conversation.** The AI will:
   - Introduce the library assumptions
   - Guide you through 6 structured steps (see below)
   - Save your answers to `status.json` after each question
3. **Resume any time.** If you close the session, just paste the prompt again — the AI will read `status.json` and continue from where you left off.

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
