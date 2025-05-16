# Active Context: Streamlit GUI for Codebase-to-Tutorial AI

## 1. Current Work Focus
- **Initial Implementation Complete**: The first version of `streamlit_app.py` has been created.
- **Task Definition**: Develop a Streamlit application that provides a user-friendly interface for configuring and running `main.py` and displaying its output.
- **Next Immediate Step**: Update `progress.md` in the Memory Bank, then provide instructions to the user for running and testing `streamlit_app.py`.

## 2. Recent Changes
- Created `streamlit_app.py` with UI for `main.py` arguments, command execution logic, output streaming, and ZIP download functionality.
- All core Memory Bank files (`projectbrief.md`, `productContext.md`, `techContext.md`, `systemPatterns.md`) were previously updated to reflect the project's scope as a GUI for `main.py`.

## 3. Next Steps
- **Testing**:
    - User to run `streamlit run streamlit_app.py`.
    - Test with various `main.py` configurations (GitHub repo, local directory, different arguments).
    - Verify output display and streaming.
    - Verify ZIP download functionality.
- **Debugging & Refinement**: Address any issues found during testing.
- **`.clinerules` Update**: Document any learned patterns or project-specific guidelines.
- **Finalize Documentation**: Ensure all Memory Bank files are accurate post-testing.

## 4. Active Decisions & Considerations
- **Target Script**: The GUI is specifically for the `main.py` script as described in the provided `README.md`.
- **Argument Coverage**: Aim to support all CLI arguments of `main.py`.
- **Output Streaming**: This is a key feature due to `main.py`'s potentially long runtime. Research best practices for `subprocess` and Streamlit.
- **File Naming**: The Streamlit app will be named `streamlit_app.py`.
- **Path Handling**: Ensure robust handling of user-provided paths, including tilde expansion.
