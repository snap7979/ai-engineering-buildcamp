from pydantic_ai.messages import ToolCallPart


def collect_tools(result):
    return [
        part.tool_name
        for message in result.new_messages()
        for part in message.parts
        if isinstance(part, ToolCallPart)
    ]
