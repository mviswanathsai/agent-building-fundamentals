This README file was written by the agent that it describes.

## AI Coding Agent - Technical Documentation

This repository implements an AI-powered coding agent designed to operate within a software project environment. The agent interacts with the repository through a series of well-defined tools, enabling it to explore, read, and modify files as needed to fulfill user prompts.

### Core Architecture

The system is structured around a modular, tool-driven architecture that enables the agent to perform complex tasks through a sequence of well-defined operations.

#### Entry Point

The `main()` function serves as the entry point of the system. It receives a user prompt via command-line arguments and initiates a dialogue with an LLM (via Ollama) to generate a response.

- **Command Line Interface**: The agent accepts a user prompt as the first argument and an optional `--verbose` flag for detailed output.
- **System Prompt**: The agent is initialized with a detailed system prompt that defines its behavior, constraints, and interaction rules.

#### Tool Execution Flow

The agent operates in an iterative loop, where each iteration involves:

1. **LLM Response**: The agent sends the current conversation history to the LLM, which may return a response or a tool call.
2. **Tool Call Handling**: If the LLM returns a tool call, the agent executes it using the corresponding function.
3. **Response Accumulation**: The agent accumulates the final output from the LLM after all tool calls have been processed.

The agent uses a maximum of `max_iters = 400` iterations to ensure sufficient time for the LLM to generate a response.

#### Available Tools

The agent has access to four primary tools, each designed to interact with the repository:

- **`get_files_info`**: Lists files and directories in the current working directory.
- **`get_file_content`**: Reads the content of a specified file.
- **`write_file`**: Writes content to a file. This tool is conditionally blocked until at least three files have been read to prevent premature or unsafe writes.
- **`run_python`**: Executes a Python script in the working directory and returns its output.

#### Tool Execution Rules

- The agent enforces a safety rule: the `write_file` tool is only allowed to execute after at least three files have been successfully read via `get_file_content`.
- The agent tracks the number of files read (`files_read`) to enforce this rule.
- Each successful `get_file_content` call increments the `files_read` counter.

#### LLM Interaction

The agent communicates with the LLM through a series of messages in a conversation history (`messages`). Each message is structured as a JSON object with a `role` (system, user, or assistant) and a `content` field.

- The system prompt is provided at the start to define the agent's behavior.
- User prompts are appended to the conversation history.
- Assistant responses and tool call results are appended to the history.

#### Performance Metrics

The agent tracks token usage for both the user prompt and the LLM response:
- `prompt_token_count`: Number of tokens in the user prompt.
- `out_token_count`: Total number of tokens consumed by the LLM in generating the response.

When the `--verbose` flag is used, these metrics are printed to the console.

#### Configuration

The system is configured with the following parameters:

- **Model**: `qwen3:4b-instruct-2507-q4_K_M` (a 4-billion parameter instruction-tuned model).
- **Max Iterations**: 400 (maximum number of iterations before terminating the conversation).

#### Error Handling

- If the LLM returns a malformed response (missing `eval_count` or `message`), the agent prints an error and terminates.
- If the agent attempts to write to a file before reading three files, it returns an error message to prevent unsafe operations.

### Workflow Example

1. User runs: `python main.py 'List all files in the directory'`
2. Agent lists files via `get_files_info`.
3. Agent reads content of three files via `get_file_content`.
4. Agent attempts to write to a file via `write_file` — this is only allowed after three files are read.
5. Agent executes a Python script via `run_python` if needed.
6. Final response is generated and printed.

### Safety and Constraints

- The agent is designed to prevent unsafe operations by enforcing a read-before-write policy.
- All file operations are performed within the current working directory, which is set to the root of the project.
- The agent does not have direct access to repository contents; it must use tools to explore and read files.

This architecture ensures that the agent operates safely and effectively within the constraints of a real software repository environment.

## ⚠️ Known Limitations

While the agent is capable of exploring repositories, modifying code, and generating documentation, it is powered by a relatively small language model (`qwen3:4b-instruct`). As a result, several limitations are expected. These are primarily due to model capacity constraints rather than architectural issues in the agent itself.

### Path Reasoning Errors

The agent may occasionally construct incorrect file paths when attempting to read files. For example, it might infer paths such as:

```
calculator/pkg/render.py
```

instead of the correct location like:

```
pkg/render.py
```

This occurs because smaller models rely heavily on pattern completion rather than robust symbolic reasoning over directory structures.

### Repeated Tool Calls

When the agent encounters an error (for example, a file path that does not exist), it may repeatedly attempt the same failing tool call instead of changing strategy. This can lead to loops such as repeatedly calling:

```
get_file_content("calculator/pkg/render.py")
```

Guardrails in the agent loop attempt to mitigate this behavior, but this isn't very effective in giving us a better answer.

### Limited Repository Understanding

Smaller models struggle to maintain a coherent mental model of large codebases. As a result, the agent may:

* Miss relationships between modules
* Fail to follow complex import chains
* Overlook relevant files
* Stop exploring prematurely

This can reduce the completeness of generated documentation or analysis.

### Prompt Sensitivity

The agent is sensitive to how instructions are phrased. Slight variations in the user prompt can significantly affect behavior, including:

* How aggressively it explores the repository
* Whether it chooses to call tools
* Whether it prematurely produces a final response

More explicit prompts generally produce better results.

### Imperfect Planning

The model has limited capacity for long-horizon planning. This means it may:

* Take inefficient exploration paths
* Inspect files in a suboptimal order
* Miss opportunities to verify assumptions using available tools

Larger models generally perform better at structured planning.

### Limited Debugging Ability

Although the agent can execute Python scripts and tests, its ability to diagnose complex bugs is limited. It may struggle with:

* Multi-file logical errors
* Subtle runtime issues
* Complex dependency chains

### Inconsistent Error Recovery

When a tool call fails, the agent may not always recover optimally. Instead of revisiting the repository structure to correct its assumptions, it may continue attempting variations of an incorrect action.

---

## Why These Limitations Exist

These behaviors are primarily a consequence of the **small model size (4B parameters)**. Larger models tend to perform better at:

* maintaining state across long tool-use sequences
* reasoning about filesystem structure
* planning multi-step actions
* recovering from errors

Despite these limitations, the agent still demonstrates useful capabilities for repository exploration, lightweight code modifications, and automated documentation generation.

---


