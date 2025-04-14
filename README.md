# OnlineCompiler

This project provides a secure, containerized environment for running user-submitted code in **Python**, **C++**, and **JavaScript**. It uses **Docker** containers for sandboxing, **Celery** for asynchronous task management, and **Redis** for message brokering and state storage.

Below is a high-level overview of each file, along with **specific code blocks** that illustrate the key functionality (without copying entire files). 

# Frontend

## Overview

This frontend is a **React** application that provides an online code editor and runner interface. Users can:

- Select a programming language (Python, JavaScript, or C++)  
- Write or paste code in a Monaco-based editor  
- Provide custom input to their program  
- Receive execution results in real time  

Styling is handled by **Tailwind CSS** and additional custom CSS files. Configuration includes **Webpack** overrides for browser compatibility and environment variable management.

---

## Table of Contents

1. [Project Structure](#project-structure)  
2. [Tech Stack](#tech-stack)  
3. [Installation](#installation)  
4. [Scripts](#scripts)  
5. [Key Files & Folders](#key-files--folders)  
   - [Tailwind Setup](#tailwind-setup)  
   - [Webpack Overrides](#webpack-overrides)  
   - [App.js](#appjs)  
   - [Index Files](#index-files)  
   - [Themes & Styling](#themes--styling)  
   - [Language Selection](#language-selection)  
   - [Code Execution Components](#code-execution-components)  
   - [Utility Hooks & Functions](#utility-hooks--functions)  
   - [Custom Input & Output](#custom-input--output)  
   - [Footer & Other UI Elements](#footer--other-ui-elements)  
6. [Running the App](#running-the-app)  
7. [Environment Variables](#environment-variables)  
8. [Contributing](#contributing)  
9. [License](#license)

---

## Project Structure

A representative structure for the frontend part of this project may look like this:

```
frontend/
├─ src/
│  ├─ components/
│  │  ├─ Landing.jsx
│  │  ├─ OutputWindow.js
│  │  ├─ OutputDetails.js
│  │  ├─ CustomInput.js
│  │  ├─ Footer.js
│  │  ├─ ...
│  ├─ constants/
│  │  ├─ languageOptions.js
│  │  ├─ customStyles.js
│  ├─ utils/
│  │  ├─ defineTheme.js
│  │  ├─ general.js
│  │  ├─ useKeyPress.js
│  ├─ App.js
│  ├─ index.js
│  ├─ index.css
│  ├─ tailwind.config.js
├─ public/
├─ package.json
├─ package-lock.json
├─ config-overrides.js
└─ ...
```

- **`src/`**: All React source code.
- **`components/`**: UI components (landing page, editor output, custom input, etc.).
- **`constants/`**: Helper objects like `languageOptions` and styling definitions.
- **`utils/`**: Shared utility functions and hooks.
- **`index.css`, `tailwind.config.js`**: Global CSS & Tailwind configuration.
- **`config-overrides.js`**: Webpack overrides for browser polyfills.
- **`package.json`**: Project dependencies and scripts.

---

## Tech Stack

1. **React** (v18+)  
2. **Tailwind CSS** (v3)  
3. **Monaco Editor** (via `@monaco-editor/react`)  
4. **Axios** for making HTTP requests  
5. **React Toastify** for notification toasts  
6. **WebSockets** for real-time updates (optional usage)  

---

## Installation

1. **Clone the repository** (or download) to your local machine.  
2. Navigate into the `frontend` directory:
   ```bash
   cd frontend
   ```
3. Install dependencies:
   ```bash
   npm install
   ```
   or
   ```bash
   yarn
   ```

---

## Scripts

Within `package.json`, you’ll find the following commonly used scripts:

- **`npm start`** – Starts the local development server.  
- **`npm run build`** – Builds the production-ready static files.  
- **`npm run test`** – Launches the test runner.  
- **`npm run eject`** – Ejects from Create React App configuration (not recommended unless necessary).

---

## Key Files & Folders

### Tailwind Setup

- **`tailwind.config.js`**  
  ```js
  // @type {import('tailwindcss').Config}

  module.exports = {
    content: ["./src/**/*.{js,jsx,ts,tsx}"],
    theme: {
      extend: {},
    },
    plugins: [],
  }
  ```
  Configures Tailwind to scan all `./src/**/*` files.

- **`index.css`**  
  ```css
  @tailwind base;
  @tailwind components;
  @tailwind utilities;

  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  body {
    font-family: karla, sans-serif;
  }
  ```
  Imports Tailwind’s base, components, and utilities layers. Also applies global resets.

### Webpack Overrides

- **`config-overrides.js`**  
  ```js
  const webpack = require('webpack');

  module.exports = function override(config) {
      const fallback = config.resolve.fallback || {};
      Object.assign(fallback, {
          "crypto": require.resolve("crypto-browserify"),
          "stream": require.resolve("stream-browserify"),
          // ...other polyfills
      })
      config.resolve.fallback = fallback;
      config.plugins = (config.plugins || []).concat([
          new webpack.ProvidePlugin({
              process: 'process/browser',
              Buffer: ['buffer', 'Buffer']
          })
      ])
      return config;
  }
  ```
  This ensures Node-specific modules (e.g., `crypto`) have browser-safe polyfills in the React environment.

### App.js

- **`App.js`**  
  ```jsx
  import Landing from './components/Landing';

  function App() {
    return (
      <>
        <Landing />
      </>
    );
  }

  export default App;
  ```
  This file is the root-level component that renders the main `<Landing />` component. It can also wrap context providers, global layout, etc.

### Index Files

- **`index.js`**  
  ```jsx
  import React from 'react';
  import ReactDOM from 'react-dom/client';
  import App from './App';
  import './components/Landing.css';
  import './index.css';

  const root = ReactDOM.createRoot(document.getElementById('root'));
  root.render(
    <React.StrictMode>
      <App />
    </React.StrictMode>
  );
  ```
  Boots up the React application and attaches it to a DOM element with `id="root"`.

### Themes & Styling

- **`defineTheme.js`**  
  ```js
  import { loader } from "@monaco-editor/react";
  import monacoThemeList from "monaco-themes/themes/themelist.json";

  // Map of theme keys to a friendly name
  const monacoThemes = {
      monokai: "Monokai",
      // etc...
  };

  const defineTheme = (theme) => {
      return new Promise((res) => {
          Promise.all([
              loader.init(),
              import(`monaco-themes/themes/${monacoThemes[theme]}.json`),
          ]).then(([monaco, themeData]) => {
              monaco.editor.defineTheme(theme, themeData);
              res();
          });
      });
  };

  export { defineTheme };
  ```
  Dynamically imports theme JSON files at runtime and registers them with Monaco.

- **`general.js`**  
  ```js
  export const classnames = (...args) => {
      return args.join(" ");
  };
  ```
  A tiny helper for concatenating CSS classes.

### Language Selection

- **`languageOptions.js`**  
  ```js
  export const languageOptions = [
    {
      id: 63,
      name: "JavaScript (Node.js 12.14.0)",
      label: "JS",
      value: "javascript",
    },
    {
      id: 54,
      name: "C++ (GCC 9.2.0)",
      label: "C++",
      value: "cpp",
    },
    {
      id: 71,
      name: "Python (3.8.1)",
      label: "Python",
      value: "python",
    },
  ];
  ```
  Lists each supported language with an `id` (matching the backend), human-readable `name`, and value for Monaco Editor.

- **`LanguagesDropdown.js`**  
  ```jsx
  import React from "react";
  import { languageOptions } from "../constants/languageOptions";
  import './MyDict.css';

  const LanguagesDropdown = ({ onSelectChange, theme }) => {
    return (
      <div className={`languagesDropdownButton ${theme}`}>
        <div>
          {languageOptions.map((option, index) => (
            <label key={option.value}>
              <input
                type="radio"
                name="radio"
                defaultChecked={index === 1}
                onChange={() => onSelectChange(option)}
              />
              <span>{option.label}</span>
            </label>
          ))}
        </div>
      </div>
    );
  };

  export default LanguagesDropdown;
  ```
  Renders a set of radio buttons for each language option.

### Code Execution Components

- **`OutputDetails.js`**  
  ```jsx
  import React from "react";

  const OutputDetails = ({ outputDetails }) => {
      return (
          <div className="metrics-container mt-4 flex flex-col space-y-3">
              <p className="text-sm">
                  Status:{" "}
                  <span className="font-semibold px-2 py-1 rounded-md bg-gray-100">
                      {outputDetails?.status?.description}
                  </span>
              </p>
              <p className="text-sm">
                  Memory:{" "}
                  <span className="font-semibold px-2 py-1 rounded-md bg-gray-100">
                      {outputDetails?.memory}
                  </span>
              </p>
              <p className="text-sm">
                  Time:{" "}
                  <span className="font-semibold px-2 py-1 rounded-md bg-gray-100">
                      {outputDetails?.time}
                  </span>
              </p>
          </div>
      );
  };

  export default OutputDetails;
  ```
  Displays output metadata like status, memory usage, and time.

- **`OutputWindow.js`**  
  ```jsx
  import React, { useState, useRef } from "react";

  const OutputWindow = ({ outputDetails, showCopyToast }) => {
    const [fontSize, setFontSize] = useState(16);
    const outputRef = useRef(null);

    const handleIncreaseFont = () => {
      setFontSize((prev) => prev + 2);
    };

    const handleDecreaseFont = () => {
      setFontSize((prev) => prev - 2);
    };

    const handleCopy = () => {
      const textToCopy = `${outputDetails?.output}\n${outputDetails?.status}\n${outputDetails?.time}\n${outputDetails?.memory}`;
      navigator.clipboard.writeText(textToCopy)
        .then(() => {
          showCopyToast('Copy output!');
        })
        .catch((err) => {
          console.error("Error with copy:", err);
        });
    };

    const handleScrollToBottom = () => {
      if (outputRef.current) {
        outputRef.current.scrollTop = outputRef.current.scrollHeight;
      }
    };

    return (
      <div className="output-container">
        <div className="button-column">
          <button onClick={handleIncreaseFont} title='Increase'>➕</button>
          <button onClick={handleDecreaseFont} title='Decrease'>➖</button>
          <button onClick={handleCopy} title='Copy'>📋</button>
          <button onClick={handleScrollToBottom} title='Down the text'>⬇</button>
        </div>
        <div
          className="output-block"
          ref={outputRef}
          style={{ fontSize: `${fontSize}px`, overflowY: "auto", maxHeight: "300px" }}
        >
          <pre>
            {outputDetails?.output}
            <p>{outputDetails?.status}</p>
            <p>{outputDetails?.time}</p>
            <p>{outputDetails?.memory}</p>
          </pre>
        </div>
      </div>
    );
  };

  export default OutputWindow;
  ```
  Provides a resizable, scrollable window for displaying execution output.

### Utility Hooks & Functions

- **`useKeyPress.js`**  
  ```js
  import React, { useState } from "react";

  const useKeyPress = function (targetKey) {
    const [keyPressed, setKeyPressed] = useState(false);

    function downHandler({ key }) {
      if (key === targetKey) {
        setKeyPressed(true);
      }
    }

    const upHandler = ({ key }) => {
      if (key === targetKey) {
        setKeyPressed(false);
      }
    };

    React.useEffect(() => {
      document.addEventListener("keydown", downHandler);
      document.addEventListener("keyup", upHandler);
      return () => {
        document.removeEventListener("keydown", downHandler);
        document.removeEventListener("keyup", upHandler);
      };
    });

    return keyPressed;
  };

  export default useKeyPress;
  ```
  Allows you to detect keyboard presses on a specific key.

### Custom Input & Output

- **`CustomInput.js`**  
  ```jsx
  import React from 'react'
  import { classnames } from '../utils/general'

  const CustomInput = ({ customInput, setCustomInput }) => {
    return (
      <>
        <textarea
          rows="5"
          value={customInput}
          onChange={(e) => setCustomInput(e.target.value)}
          placeholder="Custom Input"
        ></textarea>
      </>
    )
  }

  export default CustomInput;
  ```
  Lets the user provide input data to be fed to the code at runtime.

### Footer & Other UI Elements

- **`Footer.js`**  
  ```jsx
  import React from "react";
  import { FaGithub, FaLinkedin } from "react-icons/fa";

  const Footer = () => {
    return (
      <footer className="bg-primary bg-pattern py-4">
        <div className="container mx-auto px-4">
          <div className="flex flex-col items-center gap-y-2 justify-center">
            <div className="flex gap-x-3 text-lg text-black">
              <a href="https://github.com/eraydmrcoglu">
                <FaGithub size={20} />
              </a>
              <a href="https://www.linkedin.com/in/eraydemircioglu/">
                <FaLinkedin size={20} />
              </a>
            </div>
            <div className="text-black font-medium text-sm">
              &copy; 2023. All rights reserved.
            </div>
          </div>
        </div>
      </footer>
    );
  };

  export default Footer;
  ```
  A simple footer with social links.

---

## Running the App

1. **Ensure Dependencies** are installed (`npm install`).  
2. **Run the development server**:
   ```bash
   npm start
   ```
   This will open [http://localhost:3000](http://localhost:3000) by default.

3. (Optional) **Build for production**:
   ```bash
   npm run build
   ```
   This bundles and optimizes all assets into a `build/` folder, suitable for deployment.

---

## Environment Variables

You can create a `.env` file at the root of your frontend folder to handle environment variables. For example:

```bash
REACT_APP_API_URL=http://localhost:8000
```
- **`REACT_APP_API_URL`** – Used to point your frontend to the backend API (FastAPI).

> Note: Variables in React must begin with `REACT_APP_` to be accessible via `process.env`.

---

## Contributing

1. **Fork** the repository.
2. **Create a new branch** for your feature:
   ```bash
   git checkout -b my-feature
   ```
3. **Commit your changes**:
   ```bash
   git commit -m "Add a new feature"
   ```
4. **Push** to your branch:
   ```bash
   git push origin my-feature
   ```
5. Create a **Pull Request** in the main repository.

---

##

This React frontend, in tandem with a backend powered by FastAPI, Celery, and Docker, provides a robust platform for writing and executing code in various languages. Tailwind helps with rapid styling, while Monaco Editor offers a versatile code-editing experience. Enjoy coding!

##
# Backend

---

## 1. `main.py`

**Purpose:**  
- A FastAPI application that receives code submissions and dispatches them to Celery.  
- It also provides an endpoint to retrieve results from the Celery task queue.  
- Uses WebSockets to push results to the client in real-time.

**Key Code Block – FastAPI endpoint to submit code**:
```python
@app.post("/execute")
async def execute_code(request: dict, background_tasks: BackgroundTasks):
    """Accepts code, sends to Celery"""
    task = execute_task.delay(request)
    return {"task_id": task.id}
```

**Key Code Block – Retrieving results**:
```python
@app.get("/result/{task_id}")
async def get_result(task_id: str):
    task_result = AsyncResult(task_id)
    if task_result.state == "PENDING":
        return {"status": "processing"}
    if task_result.state == "FAILURE":
        return JSONResponse(
            status_code=500,
            content={"status": "error", "output": str(task_result.result)}
        )
    if task_result.state == "SUCCESS":
        return task_result.result
    return {"status": task_result.state.lower()}
```

---

## 2. `celery_worker.py`

**Purpose:**  
- Defines a Celery application and a task (`execute_task`) to process the user’s code.  
- Depending on the language, it delegates execution to different “runner” functions (Python, C++, JavaScript).  

**Key Code Block – Celery task**:
```python
@celery_app.task(bind=True)
def execute_task(self, request):
    language_id = request.get('language_id')
    if language_id == 71:
        result = run_py(request)
    elif language_id == 63:
        result = run_js(request)
    elif language_id == 54:
        result = run_cpp(request)
    else:
        result = {
            "output": "language not found",
            "status": "error",
        }
    redis_pub.publish(f"task:{self.request.id}", json.dumps(result))
    return result
```
Here, `run_py`, `run_js`, and `run_cpp` are invoked based on the provided `language_id`.

---

## 3. `docker-compose.yml`

**Purpose:**  
- Spins up containers for the FastAPI backend, Celery worker, Redis, and separate sandbox containers for each supported language.

**Key Code Block – Services**:
```yaml
services:
  backend:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    depends_on:
      - redis
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload

  celery:
    build: .
    command: celery -A celery_worker.celery_app worker --loglevel=info
    volumes:
      - .:/app
    depends_on:
      - redis

  redis:
    image: redis:7

  sandbox_python:
    build:
      context: ./sandbox/python

  sandbox_cpp:
    build:
      context: ./sandbox/cpp

  sandbox_js:
    build:
      context: ./sandbox/js
```
Each sandbox container (`sandbox_python`, `sandbox_cpp`, `sandbox_js`) is defined for isolated code execution.

---

## 4. Sandbox Runners

The following files define functions to handle code safety checks and to run code in Docker.

### 4.1 `pyCompile.py`

**Purpose:**  
- Checks AST for dangerous imports or functions and invokes a generic run-in-docker function.

**Key Code Block – AST checks**:
```python
def check_python_ast(source_code: str) -> str | None:
    tree = ast.parse(source_code)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            ...
        elif isinstance(node, ast.ImportFrom):
            ...
        elif isinstance(node, ast.Call):
            ...
    return None
```

**Key Code Block – Running Python code**:
```python
def run_py(request):
    source_code = request["source_code"]
    safety_error = check_python_ast(source_code)
    if safety_error:
        return { "output": safety_error, "status": "failed", "time": "0 sec" }
    result = run_code_in_sandbox(source_code, "py")
    ...
```

---

### 4.2 `cppCompile.py`

**Purpose:**  
- Performs string-based checks for forbidden headers and functions before calling the sandbox.

**Key Code Block – Header/function checks**:
```python
FORBIDDEN_HEADERS = {"fstream", "sstream", ...}
FORBIDDEN_FUNCTIONS = {"system(", "popen(", ...}

def check_code_safety(source_code):
    for header in FORBIDDEN_HEADERS:
        if f"#include <{header}>" in source_code:
            return f"Error: Use of forbidden library {header}!"
    for func in FORBIDDEN_FUNCTIONS:
        if func in source_code:
            return f"Error: Use of prohibited function {func}!"
    return None
```

**Key Code Block – Running C++ code**:
```python
def run_cpp(request):
    source_code = request["source_code"]
    safety_error = check_code_safety(source_code)
    if safety_error:
        ...
    result = run_code_in_sandbox(source_code, "cpp")
    ...
```

---

### 4.3 `jsCompile.py`

**Purpose:**  
- Checks code for banned modules or functions and delegates execution to the sandbox.

**Key Code Block – Checking dangerous code**:
```python
FORBIDDEN_MODULES = {"fs", "child_process", "os", ...}

def check_code_safety(source_code):
    if any(module in source_code for module in FORBIDDEN_MODULES):
        return "Error: Using prohibited modules!"
    if "require(" in source_code or "import " in source_code:
        return "Error: Use of `require()` and `import` is not allowed!"
    if "eval(" in source_code:
        return "Error: Use of `eval()` is prohibited!"
    return None
```

**Key Code Block – Running JS code**:
```python
def run_js(request):
    source_code = request["source_code"]
    safety_error = check_code_safety(source_code)
    if safety_error:
        ...
    result = run_code_in_sandbox(source_code, "js")
    ...
```

---

## 5. `run_in_docker.py`

**Purpose:**  
- Contains a generic function to run the code in an appropriate sandbox container using Docker CLI commands.  
- Limits memory, CPU, and network access for security.  
- Collects stdout and stderr for returning back to the user.

**Key Code Block – Docker-based sandbox**:
```python
def run_code_in_sandbox(code: str, lang: str) -> dict:
    temp_dir = "./sandbox/temp"
    ...
    docker_cmd = [
        "docker", "run", "--rm",
        "--network=none", "--memory=128m", "--cpus=0.5",
        "-v", f"{os.path.abspath(temp_code_file)}:/sandbox/{target_file}",
        docker_image
    ]
    try:
        result = subprocess.run(
            docker_cmd, capture_output=True, text=True, timeout=10
        )
        ...
    except subprocess.TimeoutExpired:
        ...
    except Exception as e:
        ...
```

This runs code in an isolated Docker container (`sandbox_python`, `sandbox_cpp`, or `sandbox_js`) with restricted resources and no network.

---

## How the Flow Works

1. **User Submits Code**  
   A user sends code (plus a language identifier) to the `/execute` endpoint in `main.py`.

2. **Celery Receives Task**  
   The code submission is passed to Celery (`execute_task` in `celery_worker.py`).

3. **Language-Specific Execution**  
   - Based on the `language_id`, Celery routes the code to `run_py`, `run_js`, or `run_cpp`.  
   - Each function performs safety checks and calls `run_code_in_sandbox` (in `run_in_docker.py`).

4. **Docker Sandbox**  
   - The user’s code is written to a temporary file in the relevant language directory.  
   - A Docker container is spun up, and the code is run with limited memory, CPU, and no network.

5. **Result Published**  
   - When execution finishes (or times out), the result is published to Redis.  
   - The FastAPI application can then retrieve these results by polling `GET /result/{task_id}` or via WebSocket.

---

## Conclusion

This setup enables a secure, scalable, and asynchronous environment for executing untrusted code in multiple languages. The system leverages Docker containers to isolate processes, Celery and Redis for task management, and FastAPI for an interface to external clients.


# with love vzbb
