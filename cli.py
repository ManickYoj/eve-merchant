import retrievedata
import displaydata
import click


@click.command()
@click.argument('origin')
@click.argument('destination')
@click.option('--refresh', is_flag=True)
@click.option('--sort-by', default='TA margin')
def main(origin, destination, refresh, sort_by):
  if refresh:
    retrievedata.run()

  click.echo(displaydata.run(origin, destination, sort_by=sort_by))


if __name__ == "__main__":
  main()
