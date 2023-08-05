import click

from person.descriptor import get_description


@click.command()
@click.option("--age", help="Person age to get description.")
def start_app(age: int = None):
    try:
        age_int = int(age)
    except (ValueError, TypeError):
        print("Podana wartość nie jest liczbą!")
        return

    if age_int < 1:
        print("Podany wiek jest mniejszy od 1")
        return

    print(f"Podana grupa wiekowa to: {get_description(age_int)}")


if __name__ == '__main__':
    start_app()
