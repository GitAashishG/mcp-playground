import asyncio
# Need to adjust sys.path if running client.py directly from its own directory
# to find the robot_mcp package, or run from the root directory.
# For simplicity when running main.py, this direct manipulation of sys.path might not be needed
# if main.py handles the package context correctly.
import sys
import os
# Add project root to sys.path to allow imports from agent
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from robot_mcp.agent.robot_agent import RobotAgent # Ensure this import works

async def run_mcp_loop(agent: RobotAgent, target_destination: str):
    print(f"CLIENT: Starting MCP loop. Target destination: {target_destination}")
    
    max_attempts = 3 # To prevent infinite loops in this example
    attempts = 0
    current_location = "" # Initialize current_location

    while attempts < max_attempts:
        attempts += 1
        print(f"\nCLIENT: Attempt {attempts}")

        # 1. Sense
        current_location = await agent.sense()
        print(f"CLIENT (Sense): Current robot location is {current_location}")

        if current_location == target_destination:
            print(f"CLIENT: Robot has reached the destination: {target_destination}")
            break
        
        # 2. Think
        print(f"CLIENT (Think): Robot is not at {target_destination}. Calculating route...")
        route = await agent.think(destination=target_destination, origin=current_location)
        print(f"CLIENT (Think): Calculated route: {route}")

        # 3. Act
        print(f"CLIENT (Act): Instructing robot to follow the route.")
        action_result = await agent.act(route=route)
        print(f"CLIENT (Act): Action result: {action_result}")

        # For this example, our mock 'act' function directly says "Reached destination".
        # In a real scenario, 'sense' in the next loop iteration would confirm this.
        if "Reached destination" in action_result:
             # We need to call sense one more time to confirm
             current_location = await agent.sense() # SENSE AGAIN
             print(f"CLIENT (Sense after Act): Current robot location is {current_location}")
             if current_location == target_destination : # Assuming act directly moves to target for mock
                print(f"CLIENT: Robot has confirmed reaching the destination: {target_destination}")
                break
             else:
                 # This case might happen if the act tool doesn't guarantee reaching the destination
                 # or if the sense tool has a more nuanced way of reporting location.
                 # For our current mock, this branch is less likely if act always "succeeds".
                 print(f"CLIENT: Act completed, but robot not yet at {target_destination}. Current location: {current_location}")


    if attempts >= max_attempts: # This line is now exactly as in the subtask description
        print(f"CLIENT: Maximum attempts reached. Robot may not have reached {target_destination}.")

async def main():
    robot_agent = RobotAgent()
    target = "Waypoint A" # The destination we want the robot to reach

    # In our mock RobotNativeFunctions, get_current_location always returns "(0,0)"
    # and follow_trajectory always returns "Move complete. Reached destination."
    # AND calculate_route takes origin and destination.
    # For the loop to work as intended, the "act" should ideally change the state
    # that "sense" reads.
    # Let's adjust the target for the sake of this simple example to match what
    # the mock `follow_trajectory` implies, or adjust `follow_trajectory`
    # For now, we'll assume `follow_trajectory` moves it to "Waypoint A"
    # and `sense` will reflect this IF the state was shared.
    # Since state isn't shared, we'll rely on the act_tool's output.
    # The native `get_current_location` will always return "Waypoint (0,0)".
    # The native `follow_trajectory` will always return "Move complete. Reached destination.".
    # This means the loop will run, `act` will claim it reached, but `sense` in the next iteration
    # won't reflect a new location unless we modify RobotNativeFunctions to simulate state change.

    # For this version, let's assume the target destination is what `calculate_route` uses.
    # And `follow_trajectory` is supposed to take it there.
    # The `sense` tool is the one that needs to reflect that change.
    # To make the loop terminate correctly with current mocks:
    # We will make the `RobotNativeFunctions.get_current_location` a bit smarter for the demo,
    # or the client will have to rely on the `act` output.
    # Let's modify `RobotNativeFunctions` in the next step if needed.
    # For now, the client will run the loop and we'll observe its behavior.

    await run_mcp_loop(agent=robot_agent, target_destination=target)

if __name__ == '__main__':
    # This allows running client.py directly for testing if needed.
    # However, the intended execution is via main.py in the root.
    # asyncio.run(main()) # Comment out for non-direct execution
    pass
