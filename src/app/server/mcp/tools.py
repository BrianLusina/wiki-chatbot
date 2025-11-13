from typing import Dict, List, Union
from app.server.mcp.server import app
import wikipedia



@app.tool()
def fetch_wikipedia_information(query: str) -> Dict[str, str]:
    """
    Search Wikipedia for a topic and return title, summary, and URL of the best match.
    """
    try:
        search_results = wikipedia.search(query)
        if not search_results:
            return {"error": "No results found for your query."}

        best_match = search_results[0]
        page = wikipedia.page(best_match)

        return {
            "title": page.title,
            "summary": page.summary,
            "url": page.url
        }

    except wikipedia.DisambiguationError as e:
        return {
            "error": f"Ambiguous topic. Try one of these: {', '.join(e.options[:5])}"
        }

    except wikipedia.PageError:
        return {
            "error": "No Wikipedia page could be loaded for this query."
        }


@app.tool()
def list_wikipedia_sections(topic: str) -> Dict[str, Union[str, List[str]]]:
    """
    Return a list the section titles from the Wikipedia page of a given topic
    """
    try:
        page = wikipedia.page(topic)
        sections = page.sections
        return {
            "sections": sections
        }
    except Exception as error:
        return {
            "error": str(error)
        }

@app.tool()
def get_section_content(topic: str, section_title: str) -> Dict[str, str]:
    """
    Return the content of a specific section in a Wikipedia article
    """
    try:
        page = wikipedia.page(topic)
        section_content = page.section(section_title)
        if section_content:
            return {
                "content": section_content
            }
        return {
            "error": f"Section '{section_title}' not found in article '{topic}.'"
        }
    except Exception as error:
        return {
            "error": str(error)
        }
