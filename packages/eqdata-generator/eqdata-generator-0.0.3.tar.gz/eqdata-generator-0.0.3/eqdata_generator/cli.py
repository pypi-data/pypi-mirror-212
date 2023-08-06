import click
import numpy as np

# @click.command()
# @click.option('--count',default=1,help='number of greetings.')
# @click.option('--name',prompt='your name', help='the person to greet')
# def cli(count,name):
#     for x in range(count):
#         click.echo(f"hello {name}")

@click.command()
@click.option('--min', default=10,help='lower bound of the interval')
@click.option('--max', default=50,help='upper bound of the interval')
@click.option('--count',default=1000,help='number of counts')
@click.option('--dist',type=click.Choice(['uniform','gaus','poison'],case_sensitive=False))
# @click.option('--dist',default='uniform',help='type of distribution')
def cli(min,max,count,dist):
    if dist=='uniform':
        click.echo(np.random.uniform(min,max,count))
    else:
        click.echo("I can only do uniform distribution lol")

# cli()
    
