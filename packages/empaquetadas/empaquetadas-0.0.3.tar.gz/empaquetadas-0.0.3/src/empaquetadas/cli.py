import click
import empaquetadas


@click.group()
def entrypoint():
    pass


@click.command()
@click.option("-a", "--amount", required=True, type=float)
@click.option("-i", "--initial-record", default="2020-01", show_default=True)
@click.option("-f", "--final-record", required=True)
@click.option(
    "--sp",
    is_flag=True,
    show_default=True,
    default=False,
    help="Invest dollars in S&P 500 index",
)
def invest_in_dollars(amount, initial_record, final_record, sp):
    usd_to_cop = empaquetadas.Converter(empaquetadas.samples.USD_TO_COP)
    convs = [usd_to_cop]
    if sp:
        convs.append(empaquetadas.Converter(empaquetadas.samples.SP_TO_USD))
    result = empaquetadas.get_change_in_time(amount, initial_record, final_record, convs)
    print(result)


entrypoint.add_command(invest_in_dollars)
