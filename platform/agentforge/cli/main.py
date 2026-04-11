"""AgentForge CLI — manage agents, skills, and tasks from the terminal."""
import typer
import httpx
import json
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from typing import Optional

app = typer.Typer(name='agentforge', help='AgentForge CLI — AI Agent Platform Manager')
console = Console()
API_URL = 'http://localhost:8000'


# ─── Auth ─────────────────────────────────────────────────────────────────
skills_app = typer.Typer(help='Manage skills')
agents_app = typer.Typer(help='Manage agents')
tasks_app = typer.Typer(help='Run tasks')
app.add_typer(skills_app, name='skills')
app.add_typer(agents_app, name='agents')
app.add_typer(tasks_app, name='tasks')


@app.command()
def status():
    """Check platform health."""
    try:
        r = httpx.get(f'{API_URL}/health', timeout=5)
        data = r.json()
        rprint(f'[green]✅ AgentForge API is healthy[/green]')
        rprint(f'  Version:  {data.get("version", "unknown")}')
        rprint(f'  Skills:   {data.get("skills", 0)}')
        rprint(f'  Agents:   {data.get("agents", 0)}')
    except Exception as e:
        rprint(f'[red]❌ API unreachable: {e}[/red]')


@skills_app.command('list')
def skills_list(category: Optional[str] = typer.Option(None, '--category', '-c')):
    """List all available skills."""
    params = {}
    if category:
        params['category'] = category
    try:
        r = httpx.get(f'{API_URL}/skills/', params=params, timeout=10)
        skills = r.json()
        table = Table(title='Available Skills')
        table.add_column('Name', style='cyan')
        table.add_column('Category', style='yellow')
        table.add_column('Level', style='green')
        table.add_column('Description')
        for s in skills:
            table.add_row(s['name'], s['category'], s.get('level', 'basic'), s['description'][:60])
        console.print(table)
    except Exception as e:
        rprint(f'[red]Error: {e}[/red]')


@skills_app.command('search')
def skills_search(query: str):
    """Search skills by name or description."""
    try:
        r = httpx.post(f'{API_URL}/skills/search', json={'query': query}, timeout=10)
        results = r.json()
        rprint(f'[bold]Found {len(results)} skills for "{query}":[/bold]')
        for s in results:
            rprint(f'  [cyan]{s["name"]}[/cyan] — {s["description"][:70]}')
    except Exception as e:
        rprint(f'[red]Error: {e}[/red]')


@skills_app.command('generate')
def skills_generate(description: str = typer.Argument(..., help='Natural language description of the skill')):
    """Auto-generate a new skill using LLM."""
    rprint(f'[yellow]⚡ Generating skill: "{description}"...[/yellow]')
    try:
        r = httpx.post(f'{API_URL}/skills/generate', json={'description': description}, timeout=60)
        skill = r.json()
        rprint(f'[green]✅ Skill generated: {skill["name"]}[/green]')
        rprint(f'  File: {skill.get("file_path", "N/A")}')
        rprint(f'  Category: {skill["category"]}')
    except Exception as e:
        rprint(f'[red]Error: {e}[/red]')


@agents_app.command('list')
def agents_list(token: str = typer.Option(..., '--token', '-t', envvar='AF_TOKEN')):
    """List your agents."""
    try:
        r = httpx.get(f'{API_URL}/agents/', headers={'Authorization': f'Bearer {token}'}, timeout=10)
        agents = r.json()
        table = Table(title='Your Agents')
        table.add_column('Name', style='cyan')
        table.add_column('Role', style='yellow')
        table.add_column('Framework', style='blue')
        table.add_column('Model')
        table.add_column('Skills')
        for a in agents:
            table.add_row(a['name'], a['role'], a['framework'], a['model'], str(len(a.get('skills', []))))
        console.print(table)
    except Exception as e:
        rprint(f'[red]Error: {e}[/red]')


@tasks_app.command('run')
def tasks_run(
    prompt: str = typer.Argument(...),
    agent_id: Optional[str] = typer.Option(None, '--agent', '-a'),
    token: str = typer.Option(..., '--token', '-t', envvar='AF_TOKEN'),
):
    """Submit a task and stream output."""
    rprint(f'[yellow]🚀 Running task: "{prompt[:60]}..."[/yellow]')
    try:
        payload = {'input': prompt, 'title': prompt[:100]}
        if agent_id:
            payload['agent_id'] = agent_id
        r = httpx.post(
            f'{API_URL}/tasks/',
            json=payload,
            headers={'Authorization': f'Bearer {token}'},
            timeout=120,
        )
        task = r.json()
        rprint(f'[green]✅ Task {task["id"]}[/green] — Status: {task["status"]}')
        if task.get('output'):
            rprint(f'\n[bold]Output:[/bold]\n{task["output"]}')
    except Exception as e:
        rprint(f'[red]Error: {e}[/red]')


if __name__ == '__main__':
    app()
