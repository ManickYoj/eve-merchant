import retrievedata
import displaydata
import click


@click.command()
@click.argument('origin')
@click.argument('destination')
@click.option('--refresh', is_flag=True)
def main(origin, destination, refresh):
  if refresh:
    retrievedata.run()

  click.echo(displaydata.run(origin, destination))


if __name__ == "__main__":
  main()
