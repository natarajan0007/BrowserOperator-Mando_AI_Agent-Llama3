# AI Agent Challenge: Mando - The Autonomous Browser Agent

## Overview

Mando is an AI agent developed using Llama 3 locally and deployed via the Groq API, inspired by the resourceful and autonomous character from the Disney+ Star Wars series, "The Mandalorian." The name reflects the agent's ability to independently navigate and execute tasks within a web browser environment. **Under the hood it uses [browseuse framework](https://docs.browser-use.com/) to enable browser interaction.**

Mando leverages Llama 3's natural language understanding to translate user intents into a sequence of browser actions. It provides a novel approach to browser-based web automation, moving away from traditional programming-based test case writing and embracing a more intuitive, natural language interface. This is achieved by using a ReAct pattern implemented within the `CustomController` class in `src/controller/custom_controller.py`.

## Key Features and Functionality

*   **Autonomous Browser Navigation:** Mando can autonomously navigate to specific websites and interact with web elements based on user instructions.  This is facilitated by the `CustomBrowser` class in `src/browser/custom_browser.py` using the Playwright library.
*   **Natural Language to Browser Action Translation:** Uses Llama 3 to understand user instructions in natural language and translate them into executable browser actions.  The prompts for Llama 3 are managed in `src/agent/custom_prompts.py`.
*   **ReAct Pattern Implementation:** Implements a ReAct (Reason, Act, Observe) loop using a custom controller to plan, think, observe, and execute browser actions effectively. The `CustomController` in `src/controller/custom_controller.py` orchestrates this loop.
*   **Web Automation Testing:** Enables browser-based web automation testing by allowing users to express test scenarios in natural language instead of code.
*   **Recording Features:** Records videos of the agent's actions, providing a visual record of the automation process.  This is enabled using Playwright's built-in recording capabilities and the `save_recording_path` configuration.
*   **Traceability:** Generates JSON files documenting the interaction between the user and the agent, providing a detailed audit trail for analysis and debugging. These files are stored in the `tmp/agent_history` directory.
*   **Deep Research:** Performs automated research and compiles markdown reports on specific topics. This feature utilizes recursive calls to LLM models to refine search queries.
*   **Configurable UI:** Allows users to easily adjust LLM settings, browser behavior, and other parameters through a comprehensive Gradio web interface.
*   **Browser Persistence:** The user can select the browser persistence mode through the UI. The options are "Default Mode" and "Persistent Mode", which are described in the UI section.

## How it Leverages Llama 3

Mando leverages Llama 3's capabilities in the following ways, primarily within the `CustomAgent` class (`src/agent/custom_agent.py`) and using prompts defined in `src/agent/custom_prompts.py`:

*   **Intent Understanding:** Llama 3 is used to interpret the user's natural language instructions and identify the desired outcome.  For example, if the user enters the task "Extract the product name and price from this webpage," Llama 3 is used to understand that the agent needs to find those specific pieces of information on a webpage. The specific prompt sent to Llama 3 might be: `"You are a helpful web automation assistant. Your task is to understand the user's goal: Extract the product name and price from this webpage.  What are the key pieces of information you need to find?"`
*   **Action Planning:** The agent uses Llama 3 to generate a plan of action based on the identified user intent. This plan outlines the steps required to achieve the desired outcome within the browser.  Based on the above example, Llama 3 might generate the following plan: `"1. Navigate to the specified URL. 2. Locate the HTML element containing the product name. 3. Extract the text from that element. 4. Locate the HTML element containing the product price. 5. Extract the text from that element."`
*   **Contextual Reasoning:** The agent uses custom prompts to ensure that Llama 3 considers the current browser context when generating actions. The model can then generate steps that make logical sense within the current page and other factors. For example, if the agent detects a login prompt, it can adjust its plan to first log in to the website by using a prompt: `"The webpage requires login. What steps do you need to take to log in before proceeding with the original task?"`
*   **Iterative Refinement (ReAct Loop):** Within the ReAct loop (managed by `CustomController`), Llama 3 is used to analyze the agent's observations and refine the plan as needed, ensuring that the agent stays on track to achieve its goal. For example, if an element is not found, Llama 3 can generate alternative strategies for locating it with the prompt: `"The element was not found using the initial strategy. Given the current page content [paste content here], what alternative strategy can you use to locate the element?"`

## Architecture

The project structure is organized as follows:

*   **`webui.py`:** The main entry point for the application, containing the Gradio web interface definition. This file defines the UI elements, their behavior, and the event handlers that connect the UI to the agent's core functionality.
*   **`monitor.py`:** Used for monitoring `webui.py` during local development for hot reloading on code changes.
*   **`src/`:**
    *   **`agent/`:** Contains the core agent logic:
        *   `custom_agent.py`: Defines the `CustomAgent` class, responsible for orchestrating the ReAct loop and interacting with the LLM and the browser.
        *   `custom_message_manager.py`: Manages communication and message handling within the agent, potentially handling formatting and logging of agent interactions.
        *   `custom_prompts.py`: Stores the prompts used to interact with Llama 3.  This module defines the specific prompts used for intent understanding, action planning, contextual reasoning, and iterative refinement.  The prompts are designed to guide Llama 3 towards generating appropriate actions for browser automation.
        *   `custom_views.py`: Handles the presentation of information to the user, potentially rendering the agent's internal state or displaying results in a user-friendly format within the web UI.
    *   **`browser/`:** Handles browser interaction using Playwright:
        *   `custom_browser.py`: Defines the `CustomBrowser` class, which manages the Playwright browser instance. This class provides methods for navigating to URLs, interacting with web elements, and retrieving page content.
        *   `custom_context.py`: Defines the `BrowserContextConfig` class, which configures the Playwright browser context. This includes settings for trace recording, video recording, viewport size, and other browser-specific options.
    *   **`controller/`:** Implements the ReAct loop:
        *   `custom_controller.py`: Defines the `CustomController` class, which controls the agent's decision-making process according to the ReAct pattern (Plan, Think, Observe, Execute). This class is responsible for calling the LLM, executing browser actions, and updating the agent's internal state.
    *   **`utils/`:** Contains utility functions and classes:
        *   `agent_state.py`: Defines the `AgentState` class, which manages the agent's internal state, including whether a stop request has been issued.
        *   `deep_research.py`: Implements the deep research functionality.  This module contains the logic for recursively searching the web, extracting information, and compiling a markdown report.  This feature likely requires a significant number of tokens and could be computationally expensive.
        *   `default_config_settings.py`: Provides default configuration values for the agent. This module defines the default settings for the LLM, the browser, and other parameters.
        *   `utils.py`: Contains general utility functions, including functions for interacting with LLMs (e.g., `get_llm_model`) and for capturing screenshots of the browser.
*   **`tmp/`:** Stores temporary data:
    *   `agent_history/`: Stores JSON files containing the agent's interaction history. These files provide a detailed audit trail of the agent's actions and reasoning.
    *   `deep_research/`: Stores data related to deep research tasks, potentially including intermediate search results or extracted content.
    *   `record_videos/`: Stores recorded videos of the agent's actions. These videos provide a visual record of the automation process.
    *   `traces/`: Stores Playwright traces (zip files) for debugging or analysis. These traces capture detailed information about the browser's execution.

## Model Usage Requirement Compliance

This project adheres to the AI Agent Challenge's Model Usage Requirements:

*   **Model Used:** Llama 3 (via Groq API)
*   **License:** Llama 3 is publicly available and free for modification and redistribution under the Meta Llama 3 Community License Agreement. Access to Llama 3 is facilitated through the Groq API, and usage is subject to Groq's terms of service.
*   **Transparency:** The agent's actions and reasoning are documented in the agent history (JSON files) and recorded videos, providing transparency into its decision-making process. The user interface also aims to provide clear feedback on the agent's progress, displaying the agent's current plan and observations. The `model_actions_output` and `model_thoughts_output` in the UI display the agent's internal reasoning.
*   **Ethical Use:** The agent is designed for browser automation and testing, and measures are taken to prevent misuse.
    *   **Prompt Engineering:** The prompts used to interact with Llama 3 (defined in `src/agent/custom_prompts.py`) are carefully designed to avoid generating harmful, biased, or discriminatory content. They prioritize factual accuracy and avoid sensitive topics unless explicitly requested by the user within the scope of the automation task. The prompts are designed to guide the agent towards performing specific browser actions and to avoid engaging in general conversation or generating inappropriate content.
    *   **Content Filtering:** While relying on Groq's built-in content filtering, the application could include a basic content filter in `utils.py` to check for profanity or hate speech in the user's input before it is passed to Llama 3. This is a basic initial approach, and more robust content moderation could be implemented in the future.
    *   **Limited Scope:** The agent's scope is intentionally limited to browser automation tasks. It is not designed for general-purpose conversation or information retrieval, reducing the risk of misuse. The prompts used by the agent are specifically tailored for browser interaction, and the agent lacks the functionality to engage in other types of activities.
*   **Data Privacy:** The agent stores user interaction history in JSON files, which are stored locally on the user's machine.
    *   **Local Storage:** These files are not transmitted to any third parties. They are stored locally for debugging and analysis purposes only.
    *   **User Control:** Users have the option to host the llama model on based on desired cloud provider to control data privacy. This is an advanced configuration option.
    *   **No PII Collection:** The agent does not collect any personally identifiable information (PII) unless explicitly provided by the user for the purpose of the automation task (e.g., entering a username or password into a website being tested). Any such PII is handled according to the privacy policy of the website being automated, and the agent itself does not store or transmit this information beyond the immediate automation task.
    *   **API Key Security:** The user is responsible for securely managing their Groq API key. The agent itself does not store the API key persistently. It is passed as an environment variable or through the UI during runtime.  It is crucial to avoid committing your API key to version control.

## Limitations

*   The agent's performance is dependent on the accuracy and completeness of the user's instructions. Clear and specific instructions are crucial for achieving the desired outcome. Vague or ambiguous instructions may lead to unpredictable behavior.
*   The agent may struggle with complex or ambiguous web page layouts, especially those that rely heavily on JavaScript or dynamic content loading. Websites with complex CSS selectors or frequently changing content may pose challenges.
*   The agent's reasoning capabilities are limited by the capabilities of the Llama 3 model and the design of the ReAct loop. More complex tasks may require more sophisticated reasoning and planning algorithms, potentially involving more iterations of the ReAct loop.
*   The agent relies on the Groq API for Llama 3 inference; its availability, rate limits, latency, and any changes to the Groq API terms of service may impact the agent's functionality. Users should be aware of Groq's terms of service. Unexpected outages or changes to the API could disrupt the agent's operation.
*   Due to using the Groq API, the number of requests is limited. The agent may exhibit slower performance or become temporarily unavailable if the request limit is reached. Consider implementing request caching or other optimization techniques to mitigate this limitation.
*   The security of your Groq API key is your responsibility. Do not expose your API key in your code or commit it to your repository. Use environment variables or secure configuration files to manage your API key. Consider using a secrets management service for production deployments.
*   The deep research functionality can be computationally expensive and may exceed API rate limits or token limits. The `max_search_iteration_input` and `max_query_per_iter_input` parameters should be carefully tuned to balance performance and cost.
*   When deep research is enabled vision may not be disabled as the feature is tightly coupled with vision currently

## Future Enhancements

*   Improve the agent's ability to handle complex web page layouts and dynamic content by integrating more robust web scraping techniques (e.g., using headless browser APIs more effectively) and improving its understanding of JavaScript (e.g., executing JavaScript code within the browser context).
*   Implement more sophisticated error handling and recovery mechanisms to handle unexpected events during browser automation, such as network errors, website changes, or unexpected pop-up windows. This could involve implementing retry logic, alternative action plans, or user notifications.
*   Develop a more advanced action planning algorithm that can reason about the long-term consequences of its actions and optimize for efficiency. This could involve using reinforcement learning or other AI techniques to learn optimal action sequences.
*   Add support for more advanced web automation tasks, such as form filling, data extraction, and automated testing of web applications. This could involve integrating with testing frameworks or providing a more user-friendly interface for defining complex automation scenarios.
*   Explore the use of fine-tuning Llama 3 on a dataset of web automation tasks to improve its performance and accuracy in this specific domain. This would require creating a labeled dataset of web automation examples and fine-tuning Llama 3 using appropriate techniques.
*   Provide the agent a functionality to select the model other than the Groq provided model. This would allow users to leverage other LLMs (within the ethical/license constraints of the challenge) and potentially compare performance. This would require abstracting the API calls and implementing logic to handle different LLM APIs.
*   Implement a more robust content moderation system, potentially integrating with third-party content filtering APIs (e.g., Perspective API) to provide more comprehensive protection against harmful content.
*   Add the functionality of saving and replaying the test case so user can execute later. This allows more control over browser automation.

## Installation Guide

### Prerequisites

*   Python 3.11 or higher
*   Git (for cloning the repository)
*   A Groq API key (obtainable from [Groq's website - `https://console.groq.com/playground`])
*   The Groq API base URL: `https://api.groq.com/openai/v1`

### Option 1: Local Installation

Read the [quickstart guide](https://docs.browser-use.com/quickstart#prepare-the-environment) or follow the steps below to get started.

#### Step 1: Clone the Repository
```bash
git clone https://github.com/natarajan0007/BrowserOperator-Mando_AI_Agent-Llama3.git
cd BrowserOperator-Mando_AI_Agent-Llama3
```

# Python Installation Guide

This guide provides a quick overview of how to install Python on your operating system. For detailed instructions, please visit the official Python downloads page.

## Installation Instructions

1. **Visit the Official Python Downloads Page:**

   Go to the [Python Downloads Page](https://www.python.org/downloads/).

2. **Select Your Operating System:**

   - **Windows:** Download the Windows installer and follow the instructions.
   - **macOS:** Download the macOS installer and follow the instructions.
   - **Linux:** Follow the instructions specific to your Linux distribution.

3. **Follow the Instructions:**

   Each operating system has specific steps to follow. The Python downloads page provides detailed guides for each OS.

## Verifying Installation

After installation, you can verify that Python is correctly installed by opening your terminal or command prompt and typing:

```bash
python --version  # For Windows
python3 --version  # For macOS and Linux
```
## Setting up virtual environment
Activate the virtual environment:
- Windows (Command Prompt):
```cmd
python -m venv venv
```

Activate the virtual environment:
- Windows (Command Prompt):
```cmd
.venv\Scripts\activate
```
- Windows (PowerShell):
```powershell
.\.venv\Scripts\Activate.ps1
```
- macOS/Linux:
```bash
source venv/bin/activate
```

#### Step 3: Install Dependencies
Install Python packages:
```bash
pip install -r requirements.txt
```

Install Playwright:
```bash
playwright install
```

#### Step 4: Configure Environment (Optional-if you're passing information directly on UI)
1. Create a copy of the example environment file:
- Windows (Command Prompt):
```bash
copy .env.example .env
```
- macOS/Linux/Windows (PowerShell):
```bash
cp .env.example .env
```
2. Open `.env` in your preferred text editor and add your API keys and other settings


# Run the Application
1.  **Run the WebUI:**
    After completing the installation steps above, start the application:
    ```bash
    python webui.py --ip 127.0.0.1 --port 7788
    ```
2. WebUI options:
   - `--ip`: The IP address to bind the WebUI to. Default is `127.0.0.1`.
   - `--port`: The port to bind the WebUI to. Default is `7788`.
   - `--theme`: The theme for the user interface. Default is `Ocean`.
     - **Default**: The standard theme with a balanced design.
     - **Soft**: A gentle, muted color scheme for a relaxed viewing experience.
     - **Monochrome**: A grayscale theme with minimal color for simplicity and focus.
     - **Glass**: A sleek, semi-transparent design for a modern appearance.
     - **Origin**: A classic, retro-inspired theme for a nostalgic feel.
     - **Citrus**: A vibrant, citrus-inspired palette with bright and fresh colors.
     - **Ocean** (default): A blue, ocean-inspired theme providing a calming effect.
   - `--dark-mode`: Enables dark mode for the user interface.
3.  **Access the WebUI:** Open your web browser and navigate to `http://127.0.0.1:7788`.
4.  **Using Your Own Browser(Optional):**
    - Set `CHROME_PATH` to the executable path of your browser and `CHROME_USER_DATA` to the user data directory of your browser. Leave `CHROME_USER_DATA` empty if you want to use local user data.
      - Windows
        ```env
         CHROME_PATH="C:\Program Files\Google\Chrome\Application\chrome.exe"
         CHROME_USER_DATA="C:\Users\YourUsername\AppData\Local\Google\Chrome\User Data"
        ```
        > Note: Replace `YourUsername` with your actual Windows username for Windows systems.
      - Mac
        ```env
         CHROME_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
         CHROME_USER_DATA="/Users/YourUsername/Library/Application Support/Google/Chrome"
        ```
    - Close all Chrome windows
    - Open the WebUI in a non-Chrome browser, such as Firefox or Edge. This is important because the persistent browser context will use the Chrome data when running the agent.
    - Check the "Use Own Browser" option within the Browser Settings.
5. **Keep Browser Open(Optional):**
    - Set `CHROME_PERSISTENT_SESSION=true` in the `.env` file.

3. **Browser Persistence Modes:**
   - **Default Mode (CHROME_PERSISTENT_SESSION=false):**
     - Browser opens and closes with each AI task
     - Clean state for each interaction
     - Lower resource usage

   - **Persistent Mode (CHROME_PERSISTENT_SESSION=true):**
     - Browser stays open between AI tasks
     - Maintains history and state
     - Allows viewing previous AI interactions
     - Set in `.env` file or via environment variable when starting container
