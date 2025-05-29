import asyncio
import sys # Import sys
# import os # os is not in the provided snippet, but current_dir = os.path.dirname... is.
            # To use os.path.dirname, os must be imported.
            # The prompt shows os.path.dirname in a comment, implying os would be needed if uncommented.
            # For strict adherence, I will comment out `import os` if `os.path.dirname` is only in comments.
            # However, the provided snippet also has `current_dir = os.path.dirname(os.path.abspath(__file__))`
            # which requires `os`. This seems like an inconsistency in the prompt.
            # I will include `import os` because it's required for the commented-out path logic shown.

import os # Required for os.path.abspath and os.path.dirname if those lines were active

# Ensure the robot_mcp package is discoverable if main.py is in the root
# This is usually handled by Python if the package structure is correct
# and you run python -m robot_mcp.main or similar,
# or if robot_mcp is in PYTHONPATH.
# For direct execution `python robot_mcp/main.py`, this shouldn't be an issue.

from robot_mcp.client.client import main as run_client_main # Or specific function like run_mcp_loop
from robot_mcp.agent.robot_agent import RobotAgent # If needed directly here

# A note on the mock state for the demo:
# The current RobotNativeFunctions.get_current_location always returns "Waypoint (0,0)".
# The RobotNativeFunctions.follow_trajectory always returns "Move complete. Reached destination."
# This means the client's loop will "succeed" based on the Act tool's output,
# but a subsequent Sense call in the loop would still report "(0,0)".
# The client's logic has a check:
#   if "Reached destination" in action_result:
#       current_location = await agent.sense() # This will still be (0,0)
#       if current_location == target_destination: # This comparison will fail if target_destination is "Waypoint A"
#
# To make the loop terminate "correctly" based on Sense after Act, we would need to:
# 1. Modify RobotNativeFunctions to simulate state changes (e.g., a class variable for location).
# 2. Or, the client trusts the Act tool's output if it's definitive.
#
# For this iteration, we will proceed with current mocks. The client will report what it sees.
# If a stateful mock is desired for RobotNativeFunctions, that would be an enhancement.

async def main():
    print("MAIN: Initializing Robot Agent and Client...")
    # The client's main function already creates an agent.
    # If we wanted to pass a pre-configured agent, we'd adjust client.py
    await run_client_main()
    print("MAIN: Client interaction finished.")

if __name__ == '__main__':
    # Ensure the path includes the robot_mcp directory if running directly from root
    # For example, if robot_mcp is a subdir of where you run `python main.py`
    # This structure assumes `main.py` is inside `robot_mcp` folder.
    # If `main.py` is in the parent of `robot_mcp`, then `from robot_mcp.client...` is fine.
    # Given the plan "In the root robot_mcp directory, create main.py",
    # this implies robot_mcp is the root.
    
    # If `robot_mcp` is the root, and `main.py` is directly in it,
    # then Python needs to know that `robot_mcp` itself is a package, or that
    # `agent` and `client` are findable.
    # The `__init__.py` in `robot_mcp` makes `robot_mcp` a package.
    # Running `python robot_mcp/main.py` from the directory *containing* `robot_mcp`
    # or `python main.py` from *within* `robot_mcp` directory.

    # To ensure imports work when running `python main.py` from `robot_mcp` directory:
    # Option 1: Add current dir to path if not already (often is by default)
    # current_dir = os.path.dirname(os.path.abspath(__file__))
    # if current_dir not in sys.path:
    #    sys.path.insert(0, current_dir)
    # Option 2: Rely on Python's default behavior which usually includes the script's dir.

    asyncio.run(main())
