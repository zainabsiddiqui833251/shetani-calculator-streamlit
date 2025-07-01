import re

class Runner:
    @staticmethod
    def run_sync(agent, prompt, run_config=None):
        try:
            for tool_name in agent.tools:
                if f"use the {tool_name}" in prompt:
                    tool = agent.tools[tool_name]
                    break
            else:
                return type('Result', (), {"final_output": "Tool not found"})()

            numbers = list(map(int, re.findall(r'\d+', prompt)))
            if len(numbers) < 2:
                return type('Result', (), {"final_output": "Missing numbers"})()

            a, b = numbers[0], numbers[1]
            output = tool(a, b)
            return type('Result', (), {"final_output": output})()

        except Exception as e:
            return type('Result', (), {"final_output": f"Error: {str(e)}"})()
