# Product Context: Streamlit GUI for Codebase-to-Tutorial AI

## 1. Problem Definition
The `main.py` script (Codebase-to-Tutorial AI) is a powerful tool for generating tutorials from codebases. However, it currently requires users to interact with it via the command-line interface (CLI). This can be:
- Less intuitive for users unfamiliar with CLI.
- Prone to errors when typing complex arguments.
- Lacking in visual feedback during configuration.

There is a need for a user-friendly graphical interface to make the `main.py` script more accessible and easier to use.

## 2. Solution
A Streamlit application will be developed to serve as a GUI front-end for the `main.py` script. This GUI will:
- Provide intuitive input fields for all of `main.py`'s command-line arguments.
- Validate inputs where appropriate.
- Construct the `main.py` command dynamically.
- Execute the command and display its output (stdout/stderr) within the app.
Streamlit is chosen for its rapid development capabilities and ease of creating interactive UIs with Python.

## 3. How it Should Work
- The user will launch the Streamlit application (`streamlit_app.py`).
- The app will display a form with input fields corresponding to `main.py` arguments (e.g., source type, repo/directory path, include/exclude patterns, language, etc.).
- The user will fill in these fields to configure the tutorial generation task.
- A "Generate Tutorial" button will trigger the process.
- The Streamlit app will construct the full `python main.py ...` command.
- The command will be executed in the background using `subprocess`.
- The output from `main.py` (progress, logs, errors) will be displayed in real-time or upon completion within the Streamlit interface.
- The generated tutorial files will be saved to the location specified by the user (or the default output directory).

## 4. User Experience Goals
- **Accessibility**: Make the "Codebase to Tutorial" tool usable for individuals less comfortable with CLI.
- **Ease of Configuration**: Simplify the process of setting up `main.py` arguments through a visual form.
- **Clarity**: Provide clear feedback on the execution status and output of `main.py`.
- **Efficiency**: Reduce the chance of errors in command construction.
