from typing import Annotated, List
from typing_extensions import TypedDict
from langgraph.graph.message import AnyMessage, add_messages


class State(TypedDict):
    """
    LangGraph state definition. This defines a dictionary-like structure with fixed keys and associated types, allowing
    LangGraph to validate and manage state transitions.

    TypedDict is used here to define a dictionary-like structure with specific key-value types. We use it to specify the
     shape of the LangGraph state, making the structure explicit and type-safe.

    :cvar messages: This field holds a list of AnyMessage objects (which represent user prompts, assistant replies, or
    tool invocations). We annotate it using Annotated[... , add_messages], which tells LangGraph to automatically append
    new messages to this list as the graph progresses. This is what enables stateful conversation across nodes.
    """
    # AnyMessage and add_messages: These are LangGraph utilities for working with chat messages. AnyMessage defines the
    # expected format of messages in the state, and add_messages is a built-in reducer that appends new messages to the
    # state during each turn in the graph.
    # Annotated let us attach metadata—in this case, a reducer function—to that field.
    messages: Annotated[List[AnyMessage], add_messages]