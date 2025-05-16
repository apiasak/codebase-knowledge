# Project Brief: Streamlit GUI for Codebase-to-Tutorial AI

## 1. Project Name
Streamlit GUI for Codebase-to-Tutorial AI

## 2. Core Goal
To develop a Streamlit-based Graphical User Interface (GUI) for the `main.py` script, which analyzes codebases (from GitHub or local directories) and generates tutorials.

## 3. Key Requirements
- The app must provide a user interface built with Streamlit for all supported arguments of `main.py` (e.g., `--repo`, `--dir`, `--language`, `--include`, `--exclude`, etc.).
- It must dynamically construct the correct `python main.py` command based on user inputs.
- It must execute the constructed command using Python's `subprocess` module.
- It must capture and display the standard output (stdout) and standard error (stderr) from the `main.py` script, ideally in real-time or streamed due to the potentially long-running nature of `main.py`.
- Handle file paths, including tilde expansion (`~`) for user convenience.

## 4. Target User
Users of the "Codebase to Tutorial" AI script (`main.py`) who prefer a graphical interface for configuring and running the script, rather than using the command-line interface (CLI).

## 5. Success Criteria
- A runnable Streamlit Python script (`streamlit_app.py` or similar).
- The application successfully gathers all necessary arguments for `main.py` through its UI.
- The application correctly constructs and executes the `main.py` command.
- The output (stdout/stderr) from `main.py` is clearly displayed to the user within the Streamlit app.
- The application handles potential errors from `main.py` gracefully (e.g., by displaying error messages).
