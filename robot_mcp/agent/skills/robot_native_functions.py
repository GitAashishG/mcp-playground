from semantic_kernel.skill_definition import sk_function, sk_function_context_parameter

class RobotNativeFunctions:
    @sk_function(description="Gets the current location of the robot", name="getCurrentLocation")
    def get_current_location(self) -> str:
        print("NATIVE FUNCTION: get_current_location called")
        return "Waypoint (0,0)"

    @sk_function(description="Calculates a route to the destination", name="calculateRoute")
    @sk_function_context_parameter(name="destination", description="The target destination")
    @sk_function_context_parameter(name="origin", description="The current robot location")
    def calculate_route(self, context) -> str:
        destination = context["destination"]
        origin = context["origin"]
        print(f"NATIVE FUNCTION: calculate_route called with origin: {origin}, destination: {destination}")
        return f"Calculated route from {origin} to {destination}: Move North, Turn East"

    @sk_function(description="Follows a given trajectory", name="followTrajectory")
    @sk_function_context_parameter(name="route", description="The route to follow")
    def follow_trajectory(self, context) -> str:
        route = context["route"]
        print(f"NATIVE FUNCTION: follow_trajectory called with route: {route}")
        # Simulate reaching the destination for now for simplicity in the loop
        return "Move complete. Reached destination."
