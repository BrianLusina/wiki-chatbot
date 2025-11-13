from app.servers.mcp.server import app


@app.prompt()
def highlight_sections_prompt(topic: str) -> str:
    """
    Identifies the most important sections from a Wikipedia article on the given topic.
    """
    return f"""
    The user is exploring the Wikipedia article on "{topic}".

    Given the list of section titles from the article, choose the 3–5 most important or interesting sections 
    that are likely to help someone learn about the topic.

    Return a bullet list of these section titles, along with 1-line explanations of why each one matters.
    """
