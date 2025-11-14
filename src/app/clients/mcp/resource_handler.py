import shlex


async def list_resources(session):
    """
    List all available resources on the server.
    """
    try:
        resource_response = await session.list_resources()
        if not resource_response or not resource_response.resources:
            print("No resources found on the server")
            return

        print("\nAvailable resources")
        for i, resource in enumerate(resource_response.resources, 1):
            print(f"[{i}]- {resource.name}")
        print("\nUse: /resource <name> to view its content.")
    except Exception as e:
        print(f"Failed to list resources: {str(e)}", e)


async def handle_resource(session, command):
    parts = shlex.split(command.strip())
    if len(parts) < 2:
        print("Usage: /resource <name>")
        return

    resource_id = parts[1]

    try:
        # Get all available resources
        response = await session.list_resources()
        resources = response.resources
        resource_map = {str(i + 1): r.name for i, r in enumerate(resources)}

        # Resolve name or index
        resource_name = resource_map.get(resource_id, resource_id)
        match = next((r for r in resources if r.name == resource_name), None)

        if not match:
            print(f"Resource '{resource_id}' not found.")
            return

        # Fetch resource content
        result = await session.read_resource(match.uri)

        for content in result.contents:
            if hasattr(content, "text"):
                print("\n=== Resource Text ===")
                print(content.text)

    except Exception as e:
        print("Resource fetch failed:", e)