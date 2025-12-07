import os
import django
from mcp.server.fastmcp import FastMCP
from asgiref.sync import sync_to_async

# Initialize Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GestionConference.settings")
django.setup()

# Importing Django models after initialization to avoid configuration errors
from ConferenceApp.models import Conference
from SessionApp.models import Session

# Create an MCP server
mcp = FastMCP("Conference Assistant")

# a. Tool to list all available conferences
@mcp.tool()
async def list_conferences() -> str:
    """List all available conferences."""
    
    @sync_to_async
    def _get_conferences():
        return list(Conference.objects.all())
    
    conferences = await _get_conferences()
    if not conferences:
        return "No conferences found."
    
    return "\n".join([f"- {c.name} ({c.start_date} to {c.end_date})" for c in conferences])

# b. Tool to get details of a specific conference by name
@mcp.tool()
async def get_conference_details(name: str) -> str:
    """Get details of a specific conference by name."""
    
    @sync_to_async
    def _get_conference():
        try:
            return Conference.objects.get(name__icontains=name)
        except Conference.DoesNotExist:
            return None
        except Conference.MultipleObjectsReturned:
            return "MULTIPLE"
    
    conference = await _get_conference()
    if conference == "MULTIPLE":
        return f"Multiple conferences found matching '{name}'. Please be more specific."
    if not conference:
        return f"Conference '{name}' not found."
    
    return (
        f"Name: {conference.name}\n"
        f"Theme: {conference.get_theme_display()}\n"
        f"Location: {conference.location}\n"
        f"Dates: {conference.start_date} to {conference.end_date}\n"
        f"Description: {conference.description}"
    )

# c. Tool to list sessions of a specific conference
@mcp.tool()
async def list_sessions(conference_name: str) -> str:
    """List sessions for a specific conference."""
    
    @sync_to_async
    def _get_sessions():
        try:
            conference = Conference.objects.get(name__icontains=conference_name)
            return list(conference.sessions.all()), conference
        except Conference.DoesNotExist:
            return None, None
        except Conference.MultipleObjectsReturned:
            return "MULTIPLE", None
    
    result, conference = await _get_sessions()
    if result == "MULTIPLE":
        return f"Multiple conferences found matching '{conference_name}'. Please be more specific."
    if conference is None:
        return f"Conference '{conference_name}' not found."
    
    sessions = result
    if not sessions:
        return f"No sessions found for conference '{conference.name}'."
    
    session_list = []
    for s in sessions:
        session_list.append(
            f"- {s.title} ({s.start_time} - {s.end_time}) in {s.room}\n"
            f"  Topic: {s.topic}"
        )
    
    return "\n".join(session_list)

# d. Free tool based on business logic: filter conferences by theme or date
@mcp.tool()
async def filter_conferences(theme: str = None, start_date: str = None, end_date: str = None) -> str:
    """Filter conferences by theme, start date, or end date. All parameters are optional."""
    
    @sync_to_async
    def _filter_conferences():
        from django.db.models import Q
        from datetime import datetime
        
        queryset = Conference.objects.all()
        
        if theme:
            queryset = queryset.filter(theme=theme)
        
        if start_date:
            try:
                start = datetime.strptime(start_date, "%Y-%m-%d").date()
                queryset = queryset.filter(start_date__gte=start)
            except ValueError:
                return None, "Invalid start_date format. Use YYYY-MM-DD."
        
        if end_date:
            try:
                end = datetime.strptime(end_date, "%Y-%m-%d").date()
                queryset = queryset.filter(end_date__lte=end)
            except ValueError:
                return None, "Invalid end_date format. Use YYYY-MM-DD."
        
        return list(queryset), None
    
    conferences, error = await _filter_conferences()
    if error:
        return error
    
    if not conferences:
        filters = []
        if theme:
            filters.append(f"theme={theme}")
        if start_date:
            filters.append(f"start_date>={start_date}")
        if end_date:
            filters.append(f"end_date<={end_date}")
        return f"No conferences found matching criteria: {', '.join(filters) if filters else 'all'}."
    
    result = f"Found {len(conferences)} conference(s):\n\n"
    for c in conferences:
        result += (
            f"- {c.name}\n"
            f"  Theme: {c.get_theme_display()}\n"
            f"  Location: {c.location}\n"
            f"  Dates: {c.start_date} to {c.end_date}\n\n"
        )
    
    return result.strip()

# Launch
if __name__ == "__main__":
    mcp.run(transport="stdio")
