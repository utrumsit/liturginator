#!/usr/bin/env python3
"""
Liturginator: A CLI app for Byzantine Catholic Church prayer texts.
"""

import click
import json
import os

@click.group()
def cli():
    """Liturginator CLI for prayer texts."""
    pass

@cli.command()
@click.argument('prayer', type=click.Choice(['trisagion', 'lords_prayer', 'credo', 'jesus_prayer']))
def recite(prayer):
    """Recite a specific prayer."""
    prayers = {
        'trisagion': "Holy God, Holy Mighty, Holy Immortal, have mercy on us.\n(Thrice)",
        'lords_prayer': "Our Father, who art in heaven,\nhallowed be thy name;\nthy kingdom come,\nthy will be done\non earth as it is in heaven.\nGive us this day our daily bread,\nand forgive us our trespasses,\nas we forgive those who trespass against us;\nand lead us not into temptation,\nbut deliver us from evil.",
        'credo': "I believe in one God,\nthe Father Almighty,\nMaker of heaven and earth,\nand of all things visible and invisible.\nAnd in one Lord Jesus Christ,\nthe only-begotten Son of God,\nbegotten of the Father before all worlds;\nGod of God, Light of Light,\nvery God of very God,\nbegotten, not made,\nbeing of one substance with the Father,\nby whom all things were made.",
        'jesus_prayer': "Lord Jesus Christ, Son of God, have mercy on me, a sinner."
    }
    click.echo(prayers[prayer])

@cli.command()
def list_prayers():
    """List available prayers."""
    click.echo("Available prayers:")
    click.echo("- trisagion")
    click.echo("- lords_prayer")
    click.echo("- credo")
    click.echo("- jesus_prayer")

@cli.command()
@click.option('--date', default=None, help='Date in YYYY-MM-DD format')
def daily_liturgy(date):
    """Display daily liturgy readings."""
    if date:
        click.echo(f"Daily liturgy for {date}:")
    else:
        from datetime import date
        today = date.today().strftime('%Y-%m-%d')
        click.echo(f"Daily liturgy for {today}:")
    click.echo("Gospel: John 3:16")
    click.echo("Epistle: Romans 8:28")
    click.echo("Psalm: 23")

@cli.command()
def vespers():
    """Display Vespers prayers."""
    click.echo("Vespers Prayers:")
    click.echo("Come, let us worship and bow down before Christ.")
    click.echo("Save us, O Son of God, who art risen from the dead...")
    click.echo("(Full Vespers text would be added here)")

@cli.command()
@click.option('--date', default=None, help='Date in YYYY-MM-DD format')
@click.option('--output', default=None, help='Output to Markdown file')
def matins(date, output):
    """Display or export Matins prayers."""
    from matins_logic import MatinsAssembler
    from datetime import datetime

    if not date:
        date = datetime.now().strftime('%Y-%m-%d')

    # Placeholder: determine if Lent
    is_lent = False  # TODO: implement Lent check

    assembler = MatinsAssembler(date, is_lent)
    text = assembler.assemble()

    if output:
        with open(output, 'w', encoding='utf-8') as f:
            f.write(text)
        click.echo(f"Matins exported to {output}")
    else:
        click.echo(text)

@cli.command()
@click.argument('prayer')
def favorite(prayer):
    """Mark a prayer as favorite."""
    favorites_file = 'favorites.json'
    if os.path.exists(favorites_file):
        with open(favorites_file, 'r') as f:
            favorites = json.load(f)
    else:
        favorites = []
    if prayer not in favorites:
        favorites.append(prayer)
        with open(favorites_file, 'w') as f:
            json.dump(favorites, f)
        click.echo(f"Marked '{prayer}' as favorite.")
    else:
        click.echo(f"'{prayer}' is already a favorite.")

@cli.command()
def show_favorites():
    """Show favorite prayers."""
    favorites_file = 'favorites.json'
    if os.path.exists(favorites_file):
        with open(favorites_file, 'r') as f:
            favorites = json.load(f)
        if favorites:
            click.echo("Favorite prayers:")
            for fav in favorites:
                click.echo(f"- {fav}")
        else:
            click.echo("No favorite prayers yet.")
    else:
        click.echo("No favorite prayers yet.")

@cli.command()
@click.argument('query')
def search(query):
    """Search for prayers containing the query."""
    all_prayers = {
        'trisagion': "Holy God, Holy Mighty, Holy Immortal, have mercy on us.\n(Thrice)",
        'lords_prayer': "Our Father, who art in heaven...",
        'credo': "I believe in one God...",
        'jesus_prayer': "Lord Jesus Christ, Son of God, have mercy on me, a sinner."
    }
    results = [name for name, text in all_prayers.items() if query.lower() in text.lower()]
    if results:
        click.echo(f"Found prayers matching '{query}':")
        for res in results:
            click.echo(f"- {res}")
    else:
        click.echo(f"No prayers found matching '{query}'.")

if __name__ == '__main__':
    cli()