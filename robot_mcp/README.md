# Robot MCP (Model Context Protocol) Sample

This project is a sample implementation of a Model Context Protocol (MCP) using the Semantic Kernel for Python.
It features a simple "Robot Agent" (server) and a client that instructs the robot to move to a waypoint.

The robot agent has three tools (implemented as native functions):
-   **Sense**: Simulates sensing the robot's current location.
-   **Think**: Simulates calculating a route to a destination.
-   **Act**: Simulates the robot following a trajectory.

## Project Structure

```
robot_mcp/
├── agent/
│   ├── skills/
│   │   ├── __init__.py
│   │   ├── robot_control_skill/
│   │   │   ├── __init__.py
│   │   │   ├── act_tool/
│   │   │   │   ├── config.json
│   │   │   │   └── skprompt.txt
│   │   │   ├── sense_tool/
│   │   │   │   ├── config.json
│   │   │   │   └── skprompt.txt
│   │   │   └── think_tool/
│   │   │       ├── config.json
│   │   │       └── skprompt.txt
│   │   └── robot_native_functions.py
│   ├── __init__.py
│   └── robot_agent.py
├── client/
│   ├── __init__.py
│   └── client.py
├── __init__.py
├── main.py
├── README.md
└── requirements.txt
```

## Setup

1.  **Clone the repository (or create the files as described).**
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    The `requirements.txt` file should contain:
    ```
    semantic-kernel
    ```

## Running the Sample

To run the sample, execute the `main.py` script from the `robot_mcp` directory:

```bash
python main.py
```

You should see output from the client and agent, simulating the Sense-Think-Act loop as the robot attempts to reach "Waypoint A".

## Notes on Mock Behavior

- The `Sense` tool (`get_current_location` native function) currently always returns "Waypoint (0,0)".
- The `Act` tool (`follow_trajectory` native function) currently always returns "Move complete. Reached destination." and prints the route it's supposed to follow.
- Because of this, the client loop will proceed based on the `Act` tool's affirmative response. A subsequent `Sense` call within the loop will still show the original location. The client's logic includes comments reflecting this behavior. For a more realistic simulation, the native functions would need to interact with a shared state or a more sophisticated mock environment.
