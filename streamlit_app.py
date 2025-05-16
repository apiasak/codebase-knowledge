import streamlit as st
import subprocess
import os
import shlex
import io
import zipfile
from pathlib import Path
import datetime # Added for timestamping

# Initialize session state variables
if 'output_lines' not in st.session_state:
    st.session_state.output_lines = []
if 'zip_ready' not in st.session_state:
    st.session_state.zip_ready = False
if 'zip_bytes' not in st.session_state:
    st.session_state.zip_bytes = None
if 'zip_filename' not in st.session_state:
    st.session_state.zip_filename = ""
if 'last_run_output_dir' not in st.session_state:
    st.session_state.last_run_output_dir = None
if 'process_running' not in st.session_state:
    st.session_state.process_running = False
if 'run_button_clicked_ever' not in st.session_state: # To track if a run was attempted
    st.session_state.run_button_clicked_ever = False
if 'current_output_display' not in st.session_state: # For the main output text area
    st.session_state.current_output_display = "Output will appear here..."

# --- UI SECTION ---
st.title("Codebase to Tutorial AI - GUI")

st.sidebar.header("Configuration")

# Source Configuration
source_type = st.sidebar.radio(
    "Select Source Type:",
    ("GitHub Repository", "Local Directory"),
    key="source_type"
)

repo_url = ""
github_token = ""
local_dir = ""

if source_type == "GitHub Repository":
    repo_url = st.sidebar.text_input(
        "GitHub Repository URL (e.g., https://github.com/username/repo):",
        key="repo_url"
    )
    github_token = st.sidebar.text_input(
        "GitHub Token (Optional):",
        type="password",
        help="For private repos or to avoid rate limits.",
        key="github_token"
    )
else: # Local Directory
    local_dir = st.sidebar.text_input(
        "Local Directory Path (e.g., /path/to/code or ~/code):",
        key="local_dir"
    )

# General Options
st.sidebar.subheader("General Options")
project_name = st.sidebar.text_input(
    "Project Name (Optional):",
    help="Derived from URL/directory if omitted.",
    key="project_name"
)
output_dir_input = st.sidebar.text_input(
    "Output Directory (Optional):",
    value="./output",
    help="Default: ./output",
    key="output_dir_input"
)
language = st.sidebar.text_input(
    "Tutorial Language (Optional):",
    value="Thai",
    help="Default: english",
    key="language"
)

# Filtering Options
st.sidebar.subheader("Filtering Options")
include_patterns_str = st.sidebar.text_area(
    "Include Patterns (Optional, space or newline separated):",
    value="*.py *.js *.css *.html *.txt",
    help="e.g., *.py *.js",
    key="include_patterns"
)
exclude_patterns_str = st.sidebar.text_area(
    "Exclude Patterns (Optional, space or newline separated):",
    value="media/* *__pycache__* memory-bank/* *.sqlite3 Procfile store_app/migrations/*",
    help="e.g., tests/* docs/*",
    key="exclude_patterns"
)
max_file_size_bytes = st.sidebar.number_input(
    "Max File Size (bytes, Optional):",
    min_value=0,
    value=100000, # Default from README.md (100KB)
    step=1000,
    help="Default: 100KB (100000 bytes)",
    key="max_file_size"
)

# Generation Parameters
st.sidebar.subheader("Generation Parameters")
max_abstractions = st.sidebar.number_input(
    "Max Abstractions (Optional):",
    min_value=1,
    value=10, # Default from README.md
    step=1,
    help="Default: 10",
    key="max_abstractions"
)
no_cache = st.sidebar.checkbox(
    "Disable LLM Cache (Optional)",
    value=False, # Default from README.md (caching enabled)
    help="Default: Caching is enabled.",
    key="no_cache"
)

# Execution
run_button = st.sidebar.button("Generate Tutorial", disabled=st.session_state.process_running)

# Output Display Area
st.subheader("Output from main.py:")
# output_placeholder = st.empty() # Will hold the main output text_area -- REMOVED
# download_section_placeholder = st.empty() -- REMOVED


# --- LOGIC SECTION ---
if run_button:
    st.session_state.run_button_clicked_ever = True # Mark that run has been attempted
    st.session_state.process_running = True
    st.session_state.output_lines = []
    st.session_state.zip_ready = False
    st.session_state.zip_bytes = None
    st.session_state.zip_filename = ""
    
    st.session_state.current_output_display = "Starting process...\n\n--- Log from main.py execution ---\n"

    # Validate Inputs
    if source_type == "GitHub Repository" and not repo_url.strip():
        st.error("GitHub Repository URL is required.")
        st.session_state.process_running = False
        st.stop()
    if source_type == "Local Directory" and not local_dir.strip():
        st.error("Local Directory Path is required.")
        st.session_state.process_running = False
        st.stop()

    effective_output_dir = os.path.expanduser(output_dir_input if output_dir_input.strip() else "./output")
    st.session_state.last_run_output_dir = effective_output_dir

    command = ["python", "main.py"]
    if source_type == "GitHub Repository":
        command.extend(["--repo", repo_url])
    else:
        command.extend(["--dir", os.path.expanduser(local_dir)])

    if project_name.strip():
        command.extend(["--name", project_name.strip()])
    if github_token.strip() and source_type == "GitHub Repository":
        command.extend(["--token", github_token.strip()])
    
    command.extend(["-o", effective_output_dir])

    if include_patterns_str.strip():
        patterns = [p.strip() for p in include_patterns_str.split()]
        if patterns: command.extend(["--include"] + patterns)
    if exclude_patterns_str.strip():
        patterns = [p.strip() for p in exclude_patterns_str.split()]
        if patterns: command.extend(["--exclude"] + patterns)
    
    if max_file_size_bytes != 100000:
         command.extend(["-s", str(max_file_size_bytes)])
    if language.strip().lower() != "english":
        command.extend(["--language", language.strip()])
    if max_abstractions != 10:
        command.extend(["--max-abstractions", str(max_abstractions)])
    if no_cache:
        command.append("--no-cache")

    display_source_name = ""
    if project_name.strip():
        display_source_name = project_name.strip()
    elif source_type == "GitHub Repository" and repo_url.strip():
        display_source_name = repo_url.strip()
    elif source_type == "Local Directory" and local_dir.strip():
        display_source_name = os.path.expanduser(local_dir.strip())
    else:
        display_source_name = "the specified source"

    st.info(f"🚀 Starting tutorial generation for '{display_source_name}'...")
    st.write(f"Language: {language.capitalize()}")
    
    with st.expander("Show execution details"):
        st.caption(f"Full command: `{' '.join(shlex.quote(c) for c in command)}`")
        st.caption(f"Output directory: {effective_output_dir}")

    with st.spinner(f"⏳ Generating tutorial for '{display_source_name}'... This may take several minutes. Please wait."):
        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True,
                cwd=os.getcwd()
            )
            for line in process.stdout:
                timestamp = datetime.datetime.now().strftime("%H:%M:%S")
                log_line_with_ts = f"[{timestamp}] {line}"
                st.session_state.current_output_display += log_line_with_ts
                st.session_state.output_lines.append(log_line_with_ts) # Store with timestamp too
                print(log_line_with_ts, end='') # Print to the terminal with timestamp
            
            process.wait()
            st.session_state.output_lines.append(f"\nProcess finished with exit code {process.returncode}")
            st.session_state.current_output_display += f"\nProcess finished with exit code {process.returncode}\n"

            if process.returncode == 0:
                st.success("main.py executed successfully!")
                output_dir_to_zip = Path(st.session_state.last_run_output_dir)
                zip_download_filename = "tutorial_output.zip"
                name_part = project_name.strip()
                if not name_part and source_type == "GitHub Repository" and repo_url.strip():
                    name_part = Path(repo_url.strip()).name.replace('.git', '')
                elif not name_part and source_type == "Local Directory" and local_dir.strip():
                    name_part = Path(os.path.expanduser(local_dir.strip())).name
                if name_part:
                    zip_download_filename = f"{name_part.replace(' ', '_')}_tutorial.zip"

                if output_dir_to_zip.exists() and output_dir_to_zip.is_dir() and any(output_dir_to_zip.iterdir()):
                    zip_buffer = io.BytesIO()
                    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
                        for file_path in output_dir_to_zip.rglob('*'):
                            if file_path.is_file():
                                zf.write(file_path, file_path.relative_to(output_dir_to_zip))
                    st.session_state.zip_bytes = zip_buffer.getvalue()
                    st.session_state.zip_filename = zip_download_filename
                    st.session_state.zip_ready = True
                else:
                    st.warning(f"Output directory '{output_dir_to_zip}' is empty or not found. Cannot create ZIP.")
                    st.session_state.zip_ready = False
            else:
                st.error(f"main.py failed with exit code {process.returncode}.")
                st.session_state.zip_ready = False
        except FileNotFoundError:
            error_message = f"Error: main.py not found. Make sure it's in the same directory as streamlit_app.py or adjust the path in the command. Current CWD: {os.getcwd()}"
            st.error(error_message)
            st.session_state.output_lines.append(error_message)
            st.session_state.current_output_display += error_message + "\n"
        except Exception as e:
            error_message = f"An error occurred: {e}"
            st.error(error_message)
            st.session_state.output_lines.append(error_message)
            st.session_state.current_output_display += error_message + "\n"
        finally:
            st.session_state.process_running = False
    
    st.rerun() # Moved outside and after the spinner block

# This section now handles all renderings of the main_output_display text_area
output_text_to_render = st.session_state.get('current_output_display', "Output will appear here...")

if not st.session_state.process_running and st.session_state.get("run_button_clicked_ever", False):
    if not st.session_state.current_output_display.strip() and "".join(st.session_state.output_lines).strip():
         output_text_to_render = "".join(st.session_state.output_lines)
    elif not st.session_state.current_output_display.strip() and not "".join(st.session_state.output_lines).strip() and st.session_state.get("run_button_clicked_ever", False) :
         output_text_to_render = "Process finished with no output."

st.text_area("Output:", value=output_text_to_render, height=400)

if st.session_state.get('zip_ready', False) and st.session_state.get('zip_bytes'):
    st.subheader("Download Tutorial Output")
    st.download_button(
        label="Download Output as ZIP",
        data=st.session_state.zip_bytes,
        file_name=st.session_state.zip_filename,
        mime="application/zip",
        key="download_zip_button" 
    )
