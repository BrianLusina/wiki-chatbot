from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import tools_condition, ToolNode
from app.clients.mcp.state_entity import State
from dotenv import load_dotenv

load_dotenv()


async def create_graph(session):
    # Load tools from MCP server and make them compatible with LangChain’s agent interface.
    tools = await load_mcp_tools(session)
    # LLM configuration (system prompt can be added later)
    llm = ChatOpenAI(model="gpt-4", temperature=0)
    llm_with_tools = llm.bind_tools(tools)

    # Prompt template with user/assistant chat only
    # The MessagesPlaceholder is a marker that tells LangChain where to inject dynamic chat history in the prompt.
    # It allows the model to maintain context across multiple turns of conversation.
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that uses tools to search Wikipedia."),
        MessagesPlaceholder("messages")
    ])

    # We combine the prompt and the tool-enabled model using the | operator. This composition allows us to invoke the
    # full chat logic (prompt → LLM → tool-aware response) in a single step.
    chat_llm = prompt_template | llm_with_tools

    def chat_node(state: State) -> State:
        """
        This function is used to create a node in the state graph that represents a chat with the AI.
        It takes in the current state and returns a new state with the chat messages updated.
        """
        # Run the chat logic to generate the AI's response
        # we pass the list of chat messages (from the state) to chat_llm.invoke(), which returns a new list of messages
        # including the assistant’s reply. The updated list is stored back in the state.
        response = chat_llm.invoke({"messages": state["messages"]})
        # Update the state with the new messages
        state["messages"] = response

        # We return the updated state to pass it to the next node in the graph
        return state

    # We create a new instance of StateGraph, passing our previously defined State type. This will hold the nodes and
    # transitions for our conversational flow.
    graph = StateGraph(State)
    # We register the chat_node we just defined as a named node in the graph.
    graph.add_node("chat_node", chat_node)
    # We add a ToolNode to the graph named "tool_node". This special node automatically manages tool execution based on
    # the available tool schema.
    graph.add_node("tool_node", ToolNode(tools=tools))
    #  We add an edge from the special START node to "chat_node", indicating that every conversation begins with a chat
    #  generation step.
    graph.add_edge(START, "chat_node")
    # We define conditional edges from "chat_node" based on whether a tool needs to be used. This uses tools_condition
    # to decide:
    # - Go to "tool_node" if a tool should be invoked.
    # - Otherwise, go to END if the assistant has responded and no tool is needed.
    graph.add_conditional_edges("chat_node", tools_condition, {
        "tools": "tool_node",
        "__end__": END
    })
    # We create a loop by adding an edge from "tool_node" back to "chat_node". This allows the agent to reprocess the
    # conversation after the available tool output.
    graph.add_edge("tool_node", "chat_node")

    # We compile the graph using .compile() and assign a MemorySaver() as the checkpointer. This handles storing and
    # tracking state across turns. The compiled graph is returned for use in the main program.
    return graph.compile(checkpointer=MemorySaver())