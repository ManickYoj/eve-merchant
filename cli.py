import retrievedata
import displaydata
import constants.type_ids
import click

@click.command()
@click.argument('origin')
@click.argument('destination')
@click.option('--refresh', is_flag=True)
@click.option('--sort-by', default='TA margin')
def main(origin, destination, refresh, sort_by):
  if refresh:
    retrievedata.run(
      region_names=[origin, destination],
      # item_ids=[item[0] for item in constants.type_ids.TYPE_IDS]
    )

  try:
    click.echo(displaydata.run(origin, destination, sort_by=sort_by))

  # If the file name has not been cached
  except FileNotFoundError:
    # If we haven't already, attempt to load the region data from the API and
    # then try again
    if not refresh:
      retrievedata.run(
        region_names=[origin, destination],
        # item_ids=[item[0] for item in constants.TYPE_IDS]
      )

      try:
        click.echo(displaydata.run(origin, destination, sort_by=sort_by))
      except FileNotFoundError:
        raise click.ClickException("Could not retrieve data for the requested regions.")

    # But if we already have tried loading the API, and we still can't find
    # the region, admit defeat
    else:
      raise click.ClickException("Could not retrieve data for the requested regions.")


if __name__ == "__main__":
  main()
