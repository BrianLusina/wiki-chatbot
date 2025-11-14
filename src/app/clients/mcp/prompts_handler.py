import shlex
from langchain_core.messages import HumanMessage


async def list_prompts(session):
    """
    List all available prompts and their argument structure.

    This function will call the `list_prompts` function on the given session,
    and print out the available prompts and their arguments.

    Example output:
    Available prompts and Argument structure

    Prompt: <prompt_name>
    - <arg1_name>
    - <arg2_name>
    ...

    Use: /prompt <prompt_name> "arg1" "arg2" ...
    """
    prompt_response = await session.list_prompts()

    if not prompt_response or not prompt_response.prompts:
        print("No prompts found on the server")
        return

    print("\nAvailable prompts and Argument structure")
    for prompt in prompt_response.prompts:
        print(f"\nPrompt: {prompt.name}")
        if prompt.arguments:
            for arg in prompt.arguments:
                print(f"- {arg.name}")
        else:
            print("- No arguments required")
    print("\nUse: /prompt <prompt_name> \"arg1\" \"arg2\" ...")


async def handle_prompt(session, tools, command: str, agent):
    """
    This processes user-entered prompt commands, validates inputs, retrieves the actual prompt text from the server,
    and runs it through the agent.
    """
    # We use shlex.split() to split the command into a list of arguments.
    # This allows us to safely parse user input into parts, handling quoted strings like "Alan Turing" as a single
    # argument. It’s especially useful for parsing command-line style input.
    parts = shlex.split(command.strip())
    if len(parts) < 2:
        print("Usage: /prompt <prompt_name> <arg1> <arg2> ...")
        return

    prompt_name = parts[1]
    args = parts[2:]
    try:
        # get available prompts
        prompt_def = await session.list_prompts()
        # check if the prompt exists
        match = next((p for p in prompt_def.prompts if p.name == prompt_name), None)
        if not match:
            print(f"Prompt '{prompt_name}' not found on the server")
            return
        # check arg count
        if len(args) != len(match.arguments):
            expected = ", ".join([a.name for a in match.arguments])
            print(f"Expected {len(match.arguments)} arguments: {expected}")
            return

        # build argument dictionary
        arg_values = {arg.name: value for arg, value in zip(match.arguments, args)}
        response = await session.get_prompt(prompt_name, arg_values)
        prompt_text = response.message[0].content.text

        # execute the prompt via the agent
        # HumanMessage lets us manually create chat messages that simulate a user speaking to the assistant. We use it
        # to send the rendered prompt string as input to the LLM agent.
        agent_response = await agent.ainvoke(
            {"messages": [HumanMessage(content=prompt_text)]},
            config={"configurable": {"thread_id": "wiki_session"}}
        )
        print("\n=== Prompt Response ===")
        print(agent_response["messages"][-1].content)
    except Exception as e:
        print(f"Error executing prompt: {e}")
