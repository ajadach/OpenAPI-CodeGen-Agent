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
  "check_sum_openapi_json": null,
  "language": null,
  "language_version": null,
  "http_library": null,
  "client_folder": null,
  "method_prefix": null,
  "modules": null,
  "generation": null,
  "pip_package": null,
  "robot_framework_support": null
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
       • check_sum_openapi_json: <value or "not set">
       • language             : <value or "not set">
       • language_version     : <value or "not set">
       • http_library         : <value or "not set">
       • client_folder        : <value or "not set">
       • method_prefix        : <value or "not set">
       • modules              : <value or "not set">
       • generation           : <value or "not set">
       • pip_package          : <value or "not set">
       • robot_framework_support: <value or "not set">
     ```
  2. Skip every question / sub-step whose corresponding `status.json` field is already non-null.
  3. **Immediately after displaying the summary — without waiting for any user input — ask the next unanswered question** (the first field that is still `null`).
  4. Do not repeat anything already answered. Ask only one question at a time, then wait for the user's response before proceeding.

## Step 1 — API Information

Ask the user the following questions and save the answers in `status.json`.
For each question, display the short context note below it before waiting for the answer.

1. Provide the URL to the Swagger documentation → `status.json: swagger_url`
   > This is the address of the human-readable API documentation (e.g. Swagger UI page). It is saved for reference and helps locate the `openapi.json` file in the next step.

2. Provide the main REST API endpoint → `status.json: base_endpoint`
   > This becomes the `BASE_URL` in `basic.py` and the default value in the client constructor. All generated API calls will be sent to this address. If no scheme is provided, `https://` will be added automatically — e.g. `petstore.swagger.io/v2` → `https://petstore.swagger.io/v2`.

## Step 2 — Project Structure Configuration

For each question, display the short context note below it before waiting for the answer.

1. Ask the user what the library folder should be named and save the answer in `status.json` → `status.json: library_folder`
   > This is the root folder of the entire project — it will contain the client package, swagger file, and build artifacts. The Python client package will be automatically named `{library_folder}Client`. For example: `PetStore` → root folder `PetStore/`, Python package `PetStoreClient/`.
2. Automatically derive `client_folder` as `{library_folder}Client` and save it in `status.json: client_folder` — **do not ask the user for this value**
   - Example: `library_folder = PetStore` → `client_folder = PetStoreClient`
3. Create the given folder, and inside it:
   - a `trash_AI` folder — a place where AI puts temporary files that the user does not need
   - a `swagger` folder — here the user will place the `openapi.json` file
4. Ask the user one of the following:
   - If they have the `openapi.json` file locally — ask them to place it in the `swagger` folder and type **"done"**
   - If the file is available online — ask them to provide the URL and AI will download it automatically
   - Hint to the user: *"Type 'done' if you placed the file manually, or paste a URL to download it automatically."*
5. Handle the user's response:
   - If the response starts with `http://` or `https://` — download the file automatically:
     - Use `Invoke-WebRequest -Uri "<url>" -OutFile "{library_folder}/swagger/openapi.json"` (PowerShell) or `wget -O {library_folder}/swagger/openapi.json <url>` (Linux/macOS)
     - Confirm to the user that the file was downloaded successfully
   - If the response is **"done"** — assume the file was placed manually and proceed
6. After the file is confirmed present (downloaded or manual), calculate its SHA-256 checksum:
   - PowerShell: `(Get-FileHash "{library_folder}/swagger/openapi.json" -Algorithm SHA256).Hash`
   - Linux/macOS: `sha256sum {library_folder}/swagger/openapi.json`
   - Save the resulting hash string in `status.json` → `status.json: check_sum_openapi_json`
   - Display the checksum to the user
7. Save confirmation in `status.json` → `status.json: openapi_json_confirmed`

## Step 3 — Technical Library Configuration

For each question, display the short context note below it before waiting for the answer.

1. In what programming language should the library be created? → `status.json: language`
   > All generated code, syntax, and tooling will follow this language's conventions. For Python, Pydantic will be used for argument validation and Robot Framework support will be available as an optional add-on.

2. What version of that language should it be compatible with? → `status.json: language_version`
   > This version is used in `pyproject.toml` (`requires-python`) and ensures the generated code syntax is compatible. For example: `3.12` → `requires-python = ">=3.12"`.

3. Which library should be used for making REST API requests? → `status.json: http_library`
   > This library will be imported in every generated module and used to execute all HTTP calls. It will also be listed as a dependency in `pyproject.toml`. For example: `requests`.
4. After receiving the answers, create the `{client_folder}` folder inside `{library_folder}` and create `{library_folder}/{client_folder}/basic.py` with the following content (use the value from `status.json: base_endpoint` for `BASE_URL`, adding `https://` if no scheme is present):
     ```python
     """Shared configuration for the API client.

     BASE_URL and SESSION are set by the client __init__ before any module is used.
     All modules import this module and read BASE_URL and SESSION at call time.
     """

     import requests

     BASE_URL: str = "https://{base_endpoint}"
     SESSION: requests.Session = requests.Session()
     ```
5. Should the methods in classes have a prefix matching the REST API method?

   - without prefix: `client.add_pet`
   - with prefix: `client.post_add_pet`

   → `status.json: method_prefix`
   > This affects the naming of every generated method across all modules. The prefix is the HTTP verb (`get_`, `post_`, `put_`, `delete_`). With prefix the method names are more explicit about the HTTP operation; without prefix they are shorter. This choice applies consistently to all modules.

Save the answers in `status.json`.

## Step 4 — Library Generation

1. Read the `swagger/openapi.json` file
2. Count the modules (tags) and inform the user how many were found and what their names are
3. Ask the user whether they want to generate the library for all modules or only selected ones
   - If selected — ask for the module names
   - Save the choice in `status.json` → `status.json: modules`
   > Each module corresponds to one API tag from `openapi.json` and becomes a separate Python file with its own class (e.g. tag `pet` → file `pet.py`, class `Pet`). Selecting only specific modules allows generating a partial client covering only the API resources the user needs.
4. For each selected module, set the state in `status.json: generation` to `pending`
5. Wait for user confirmation before starting code generation
6. Generate modules one by one — for each module:
   - Before starting, set the state to `in_progress` in `status.json: generation`
   - **Naming convention:** the file is named after the tag (lowercase), and the class is named after the tag in PascalCase — e.g. tag `pet` → file `pet.py`, class `Pet`; tag `store` → file `store.py`, class `Store`
   - Generate the module file at `{library_folder}/{client_folder}/modules/{module}.py`:
     - The module class must have **no constructor parameters** — do not accept `base_url` or `session`
     - Import shared config at the top: `from .. import basic`
     - Expose `_base_url` and `_session` as read-only properties:
       ```python
       @property
       def _base_url(self) -> str:
           return basic.BASE_URL

       @property
       def _session(self):
           return basic.SESSION
       ```
   - Generate `{library_folder}/{client_folder}/modules/__init__.py` exporting all module classes
   - Generate `{library_folder}/{client_folder}/client.py` — the main client file that:
     - imports `from . import basic`
     - accepts `base_url` defaulting to the value from `status.json: base_endpoint`; adds `https://` prefix if no scheme is present
     - sets `basic.BASE_URL = base_url` and `basic.SESSION = requests.Session()`
     - creates each module instance **without arguments**: `self.{module} = {ModuleClass}()`
     - **does NOT re-expose module methods** — users call `client.pet.method()`, `client.store.method()`, etc. directly
     - **no `@keyword` decorators, no `ROBOT_LIBRARY_SCOPE`, no delegation methods at this stage**
   - After completion, set the state to `done` in `status.json: generation`
7. At every start or resumption of the procedure, check `status.json: generation`:
   - Skip modules with state `done`
   - Resume from the first module with state `pending` or `in_progress`

## Step 5 — Robot Framework Support (Python only)

This step is executed only if `status.json: language` is `python`.

1. Ask the user: **"Do you want to add Robot Framework support to the library?"**
   - Save the answer in `status.json: robot_framework_support` (`true` / `false`)
   > If yes, every module method will be decorated with `@keyword` and `ROBOT_LIBRARY_SCOPE = "SUITE"` will be added to each module class. This makes each module importable as a standalone Robot Framework library — e.g. `Library    PetStoreClient.Pet` — with keywords callable as `PetStoreClient.Pet.Post Add Pet    ${pet}`.
2. If the answer is `true`:

   **2a. Add `@keyword` decorators and `ROBOT_LIBRARY_SCOPE` to every module class**

   For each file in `{library_folder}/{client_folder}/modules/` (excluding `__init__.py`):
   - Add `ROBOT_LIBRARY_SCOPE = "SUITE"` as a class attribute
   - Add import at the top of the file (after existing imports):
     ```python
     from robot.api.deco import keyword
     ```
   - Add `@keyword("<Keyword Name>")` decorator **above** the `def` line of every public method (below `@validate_call` if present)
   - Keyword name is derived from the method name by: replacing underscores with spaces, capitalizing each word
     - Example: `post_add_pet` → `"Post Add Pet"`
     - Example: `get_find_pets_by_status` → `"Get Find Pets By Status"`

   **2b. Update `{library_folder}/{client_folder}/modules/__init__.py`**

   Export the short-named classes:
   ```python
   from .pet import Pet
   from .store import Store
   from .user import User

   __all__ = ["Pet", "Store", "User"]
   ```

   **2c. Update `{library_folder}/{client_folder}/client.py`**

   - Add `__all__ = ["<ClientClass>"]` at module level (before the class definition)
   - The client class itself does **not** get `@keyword` decorators and does **not** re-expose module methods — it only holds module instances (`self.pet`, `self.store`, etc.)
   - No `ROBOT_LIBRARY_SCOPE` on the client class

   **2d. Update `{library_folder}/{client_folder}/__init__.py`**

   Replace the contents with the following structure:
   ```python
   """<ClientFolder> package."""

   import logging

   from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError

   from .client import <ClientClass>
   from .modules import <Module1Class>, <Module2Class>  # short names, e.g. Pet, Store, User

   LIBRARIES = ["<Module1Class>", "<Module2Class>"]  # short names used in import path

   RFW = BuiltIn()
   try:
       for name in LIBRARIES:
           RFW.import_library("{client_folder}." + name)
   except RobotNotRunningError:
       pass

   # initialize logging
   log = logging.getLogger(__name__)
   log.addHandler(logging.NullHandler())
   ```

   **How it works in Robot Framework:**
   ```robot
   *** Settings ***
   Library    {client_folder}            # loads PetStoreClient + auto-imports all modules
   Library    {client_folder}.Pet        # makes Pet keywords available

   *** Test Cases ***
   Example
       ${pet}=    Evaluate    {"name": "doggie", "photoUrls": [], "status": "available"}
       {client_folder}.Pet.Post Add Pet    ${pet}
   ```

   Each module is a standalone RF library. Keywords are namespaced as `{client_folder}.<ModuleName>.<Keyword Name>`.

   > **Note:** `ROBOT_LIBRARY_SCOPE` and `@keyword` decorators in module files (`modules/*.py`) are added **only** in this step — they must not appear in the generated files before the user answers "yes" to Robot Framework support.

3. If the answer is `false`:
   - Skip this step and continue

## Step 6 — pip Package (Python only)

This step is executed only if `status.json: language` is `python`.

1. Ask the user: **"Do you want to prepare the library as a ready-to-install pip package?"**
   - Save the answer in `status.json: pip_package` (`true` / `false`)
   > If yes, a `pyproject.toml` and `README.md` will be created and `python -m build` will be run to produce a `.whl` and `.tar.gz` file in the `dist/` folder. The package can then be installed in any environment with `pip install dist/<package>.whl` — no manual path setup needed.
2. If the answer is `true`:
   - Make sure the `library_folder` contains a valid `pyproject.toml` file with the following sections:
     - `[project]` — package name, version, description, author, requirements (`dependencies`)
     - `[build-system]` — `requires = ["setuptools", "wheel"]`, `build-backend = "setuptools.build_meta"`
     - `[tool.setuptools.packages.find]` — `include = ["{client_folder}*"]` (prevents setuptools from accidentally packaging unrelated top-level folders such as `swagger` or `trash_AI`)
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

## Step 7 — Archive AI Artifacts

Before displaying the success summary, copy the generation artifacts into the client package for future reference:

1. Create folder `{library_folder}/{client_folder}/AI/swagger/`
2. Copy `{library_folder}/swagger/openapi.json` → `{library_folder}/{client_folder}/AI/swagger/openapi.json`
3. Copy `status.json` → `{library_folder}/{client_folder}/AI/status.json`

These files may be used in the future to regenerate or update the library.

- PowerShell:
  ```powershell
  New-Item -ItemType Directory -Path "{library_folder}/{client_folder}/AI/swagger" -Force
  Copy-Item "{library_folder}/swagger/openapi.json" -Destination "{library_folder}/{client_folder}/AI/swagger/openapi.json"
  Copy-Item "status.json" -Destination "{library_folder}/{client_folder}/AI/status.json"
  ```
- Linux/macOS:
  ```bash
  mkdir -p {library_folder}/{client_folder}/AI/swagger
  cp {library_folder}/swagger/openapi.json {library_folder}/{client_folder}/AI/swagger/openapi.json
  cp status.json {library_folder}/{client_folder}/AI/status.json
  ```

## Step 7 — Success Summary

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
  🤖 Robot Framework  : {robot_framework_support}

To use the library:

  from {client_folder}.client import <ClientClass>
  client = <ClientClass>()

Thank you for using Open API codegen by AI! 🚀
```

- Fill in all placeholders with actual values from `status.json`
- If `robot_framework_support` is `null` (step was skipped), display `skipped`
