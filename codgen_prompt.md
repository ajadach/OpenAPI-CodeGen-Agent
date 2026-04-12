# Open API codegen by AI

**Author:** Artur Ziółkowski
**LinkedIn:** [https://www.linkedin.com/in/arturjadach/](https://www.linkedin.com/in/arturjadach/)

## Idea

Super Prompt AI Gen is an AI-driven procedure designed to replace traditional CodeGen tools
(such as swagger-codegen, openapi-generator, etc.) in the process of creating client libraries
for REST APIs.

Instead of generating code from templates — AI guides the user step by step through gathering
requirements, and then creates a project tailored to their needs.

## Information for the user

At the beginning of the procedure, inform the user of the following library assumptions:

- The library is built following the **Resource-based grouping** pattern — methods are grouped by API resource
- The library always expects a response with an HTTP status code in the 2xx range
- The library is an interface for API testing — error handling and negative cases belong in tests, not in the library

## Status

User responses collected during the procedure are saved in the `status.json` file.
AI reads and updates this file at every step of the procedure.

At the very beginning of the procedure (before Step 1), AI creates the `status.json` file with all keys set to `null`:

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

## Rules for AI

- Do not add any unnecessary print statements to the generated library
- Write code according to the standards appropriate for the given language (e.g. PEP8 for Python)
- The library is built following the **Resource-based grouping** pattern — methods are grouped by API resource (e.g. `client.pets.get_all()`, `client.orders.create(...)`)
- The library always expects an HTTP status in the 2xx range — it does not handle negative cases
- Negative request cases are handled at the test level, not in the library — the library is an interface that enables API testing
- The order of methods in classes must follow the order of endpoints in the `openapi.json` file
- If the chosen language is Python — use **Pydantic** for argument validation in methods
- Every class and every method must have a docstring with a description taken from `summary` in `openapi.json`
  - A method docstring must include: description, an `Args:` section with each parameter description and type, a `Returns:` section with a description of the return value
- Work with the user is dynamic — after every break or topic change, always return to the last unfinished step from `prompt.md`, checking the state in `status.json`
- **Never re-ask a question whose answer is already saved (non-null) in `status.json`** — treat every non-null value as confirmed and move on
- On every run, read `status.json` first; if any values are already filled in, display a **resume summary** (see *Resume Behaviour* below) instead of starting from the beginning

## Resume Behaviour

At the very start of every run, read `status.json` before doing anything else.

- If **all values are `null`** → this is a fresh start. Show the library assumptions (see *Information for the user*) and begin Step 1 from question 1.
- If **any value is non-null** → this is a resumed session. Do the following:
  1. Display a resume notice to the user, for example:
     ```
     ▶ Resuming previous session. Here is what has already been collected:
       • swagger_url          : <value or "not set">
       • base_endpoint        : <value or "not set">
       • library_folder       : <value or "not set">
       • openapi_json_confirmed: <value or "not set">
       • language             : <value or "not set">
       • language_version     : <value or "not set">
       • http_library         : <value or "not set">
       • client_folder        : <value or "not set">
       • method_prefix        : <value or "not set">
       • modules              : <value or "not set">
       • generation           : <value or "not set">
       • pip_package          : <value or "not set">
       • testpypi_upload      : <value or "not set">
     ```
  2. Skip every question / sub-step whose corresponding `status.json` field is already non-null.
  3. **Immediately after displaying the summary — without waiting for any user input — ask the next unanswered question** (the first field that is still `null`).
  4. Do not repeat anything already answered. Ask only one question at a time, then wait for the user's response before proceeding.

## Step 1 — API Information

Ask the user the following questions and save the answers in `status.json`:
Do not provide the user with any examples or hints — wait for their answer.

1. Provide the URL to the Swagger documentation → `status.json: swagger_url`
2. Provide the main REST API endpoint → `status.json: base_endpoint`

## Step 2 — Project Structure Configuration

Do not provide the user with any examples or hints — wait for their answer.

1. Ask the user what the library folder should be named and save the answer in `status.json` → `status.json: library_folder`
2. Create the given folder, and inside it:
   - a `trash_AI` folder — a place where AI puts temporary files that the user does not need
   - a `swagger` folder — here the user will place the `openapi.json` file
3. Ask the user to place the `openapi.json` file (compliant with the OpenAPI standard) in the `swagger` folder
4. Wait for confirmation from the user that the file has been created → `status.json: openapi_json_confirmed`

## Step 3 — Technical Library Configuration

Do not provide the user with any examples or hints — wait for their answer.

1. In what programming language should the library be created? → `status.json: language`
2. What version of that language should it be compatible with? → `status.json: language_version`
3. Which library should be used for making REST API requests? → `status.json: http_library`
4. What should the main folder of the library be named (where all client code will be stored)? → `status.json: client_folder`
   - After receiving the answer, create this folder inside `library_folder`
5. Should the methods in classes have a prefix matching the REST API method?

   - without prefix: `client.add_pet`
   - with prefix: `client.post_add_pet`

   → `status.json: method_prefix`

Save the answers in `status.json`.

## Step 4 — Library Generation

1. Read the `swagger/openapi.json` file
2. Count the modules (tags) and inform the user how many were found and what their names are
3. Ask the user whether they want to generate the library for all modules or only selected ones
   - If selected — ask for the module names
   - Save the choice in `status.json` → `status.json: modules`
4. For each selected module, set the state in `status.json: generation` to `pending`
5. Wait for user confirmation before starting code generation
6. Generate modules one by one — for each module:
   - Before starting, set the state to `in_progress` in `status.json: generation`
   - Generate the module file at `{library_folder}/{client_folder}/modules/{module}.py`
   - Generate `{library_folder}/{client_folder}/modules/__init__.py` exporting all module classes
   - Generate `{library_folder}/{client_folder}/client.py` — the main client file that:
     - accepts `base_url` from `status.json: base_endpoint`
     - creates a shared `requests.Session()`
     - passes `base_url` and `session` to each module
   - After completion, set the state to `done` in `status.json: generation`
7. At every start or resumption of the procedure, check `status.json: generation`:
   - Skip modules with state `done`
   - Resume from the first module with state `pending` or `in_progress`

## Step 5 — pip Package (Python only)

This step is executed only if `status.json: language` is `python`.

1. Ask the user: **"Do you want to prepare the library as a ready-to-install pip package?"**
   - Save the answer in `status.json: pip_package` (`true` / `false`)
2. If the answer is `true`:
   - Make sure the `library_folder` contains a valid `pyproject.toml` file with the following sections:
     - `[project]` — package name, version, description, author, requirements (`dependencies`)
     - `[build-system]` — `requires = ["setuptools", "wheel"]`, `build-backend = "setuptools.backends.legacy:build"`
   - Make sure the `library_folder` contains a `README.md` file with the following content:
     - **Project title** — name of the generated library
     - **Description** — what API it covers, the base endpoint, and which modules are included
     - **Requirements** — language version and HTTP library used
     - **Installation** section — two sub-sections:
       - *As a pip package* (if `pip_package` is `true`): `pip install dist/<package>.whl`
       - *Local usage without pip*: instructions to add `library_folder` to `sys.path` or run from workspace root
     - **Quick start** — a minimal working code example showing how to import and instantiate the client
     - **Modules** section — for each generated module, list:
       - Module name and its API resource description
       - All available methods with their signatures, parameters, and a one-line description
     - **Method reference** — full list of all methods across all modules, grouped by module, with parameter names, types, and return value description
     - **Environment / configuration** — explain the `base_url` parameter and how to override it if needed
     - **License** — placeholder `MIT` if not provided by the user
   - Install the `build` tool: `pip install build`
   - Build the package: `python -m build` (run inside `library_folder`)
   - Inform the user that the `.whl` and `.tar.gz` packages are available in the `dist/` folder
   - Optionally: ask the user whether they want to publish the package to TestPyPI:
     - If yes: install `twine` and run `twine upload --repository testpypi dist/*`
     - Save the decision in `status.json: testpypi_upload` (`true` / `false`)
3. If the answer is `false`:
   - Inform the user that the library can be used locally without installing via pip
   - Provide clear instructions on how to use the library locally:
     - Add the `library_folder` path to `sys.path` in the test/script file, **or**
     - Run scripts from the root of the workspace so that Python can resolve imports correctly
   - Show a ready-to-use code snippet:
     ```python
     import sys
     sys.path.insert(0, "/path/to/{library_folder}")

     from {client_folder}.client import <ClientClass>
     client = <ClientClass>()
     ```
   - Remind the user that no `pip install` is required — the library works as a local package

## Step 6 — Success Summary

After all steps are completed, display a final success message to the user in the following format:

```
╔══════════════════════════════════════════════════════════════╗
║              🎉  LIBRARY GENERATION COMPLETE!  🎉            ║
╚══════════════════════════════════════════════════════════════╝

✅ All steps finished successfully. Here is a summary of what was created:

  📁 Library folder   : {library_folder}/
  📦 Client package   : {library_folder}/{client_folder}/
  🐍 Language         : {language} {language_version}
  🌐 HTTP library     : {http_library}
  🔗 Base endpoint    : {base_endpoint}
  🧩 Modules generated: {list of modules with status "done"}
  📄 pip package      : {pip_package}
  🚀 TestPyPI upload  : {testpypi_upload}

To use the library:

  from {client_folder}.client import <ClientClass>
  client = <ClientClass>()

Thank you for using Open API codegen by AI! 🚀
```

- Fill in all placeholders with actual values from `status.json`
- If `testpypi_upload` is `null` (step was skipped), display `skipped`
- If `pip_package` is `false`, omit the TestPyPI line entirely
