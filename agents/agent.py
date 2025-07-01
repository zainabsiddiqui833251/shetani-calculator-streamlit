def function_tool(func):
    return func

class Agent:
    def __init__(self, name, instructions, tools):
        self.name = name
        self.instructions = instructions
        self.tools = {tool.__name__: tool for tool in tools}
