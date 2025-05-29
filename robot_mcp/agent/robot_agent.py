import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAITextCompletion # Placeholder for potential future use
# We will use native functions directly, so no specific model is strictly needed for this example
# from semantic_kernel.orchestration.context_variables import ContextVariables # If needed

from .skills.robot_native_functions import RobotNativeFunctions # Adjusted import path

class RobotAgent:
    def __init__(self):
        self.kernel = sk.Kernel()
        # For this example, we are not using an explicit AI model for the tools,
        # as they are backed by native functions.
        # If we were using semantic functions with prompts that need an LLM, we'd configure one here.
        # self.kernel.add_text_completion_service("dv", OpenAITextCompletion("text-davinci-003", "YOUR_OPENAI_API_KEY"))

        # Register native functions
        self.robot_functions = RobotNativeFunctions()
        # The skills_directory path for SK should be relative to where the script is run,
        # or an absolute path. For simplicity, if running from robot_mcp, this would be "agent/skills/"
        # However, semantic-kernel often expects paths relative to the CWD or absolute.
        # Given the client will run from robot_mcp root, let's adjust for that.
        self.skills_directory = "robot_mcp/agent/skills/" 
        
        # Import native skills
        self.robot_control_skill = self.kernel.import_skill(self.robot_functions, skill_name="RobotNativeFunctions")

        # If we were using semantic (prompt-based) skills, we would load them like this:
        # self.sense_tool_skill = self.kernel.import_semantic_skill_from_directory(self.skills_directory, "robot_control_skill/sense_tool")
        # self.think_tool_skill = self.kernel.import_semantic_skill_from_directory(self.skills_directory, "robot_control_skill/think_tool")
        # self.act_tool_skill = self.kernel.import_semantic_skill_from_directory(self.skills_directory, "robot_control_skill/act_tool")


    async def sense(self) -> str:
        # Directly invoking the native function registered in the kernel
        result = await self.kernel.run_async(
            self.robot_control_skill["getCurrentLocation"]
        )
        return str(result)

    async def think(self, destination: str, origin: str) -> str:
        context = self.kernel.create_new_context()
        context["destination"] = destination
        context["origin"] = origin
        
        result = await self.kernel.run_async(
            self.robot_control_skill["calculateRoute"],
            input_context=context
        )
        return str(result)

    async def act(self, route: str) -> str:
        context = self.kernel.create_new_context()
        context["route"] = route

        result = await self.kernel.run_async(
            self.robot_control_skill["followTrajectory"],
            input_context=context
        )
        return str(result)

if __name__ == '__main__':
    # Example usage (optional, for testing the agent directly)
    import asyncio

    async def main():
        # This assumes you run this script from the root of the `robot_mcp` directory
        # or that `robot_mcp` is in the Python path.
        # For direct execution from `robot_mcp/agent`, paths might need adjustment or use `sys.path.append`.
        
        # Quick way to adjust path for direct execution from agent directory for testing
        import sys
        import os
        # If running from robot_mcp/agent, add robot_mcp to path
        if os.getcwd().endswith("agent"):
             sys.path.append(os.path.dirname(os.getcwd()))


        agent = RobotAgent()
        
        current_location = await agent.sense()
        print(f"Sensed Location: {current_location}")
        
        # Example logic: if not at Waypoint A, plan and move.
        # The native function returns "Waypoint (0,0)"
        if current_location != "Waypoint A": # This condition will be true based on current mock
            destination_waypoint = "Waypoint A"
            route = await agent.think(destination=destination_waypoint, origin=current_location)
            print(f"Calculated Route: {route}")
            
            action_result = await agent.act(route=route)
            print(f"Action Result: {action_result}")
        else:
            print("Already at destination.")

    # asyncio.run(main()) # Comment out or remove for non-direct execution
