import sys

from toolforgeio import read_input_file, write_output_file, Arguments

NAMES_INPUT_FILENAME = "/tmp/names.txt"
SALUTATIONS_OUTPUT_FILENAME = "/tmp/salutations.txt"


def salutation(greeting: str, name: str):
    return f"${greeting}, ${name}!"


if __name__ == "__main__":
    # Parse our arguments
    args = Arguments.parse_from_argv(sys.argv).autospecialize()

    # It's polite to say hello!
    print(f"Hello!")

    greeting = args.get("Greeting", "Hi")
    names_input_url = args.get("Names")
    salutations_output_url = args.get("Salutations")

    # Read all the names from our input
    names = []
    with open(NAMES_INPUT_FILENAME, "wb") as f:
        read_input_file(names_input_url, f)
    with open(NAMES_INPUT_FILENAME, "r") as f:
        for line in f:
            names.append(line)

    # Tell the user we understood their inputs
    print(f"Now writing {len(names)} salutations with greeting ${greeting}...")

    # Write our program output
    with open(SALUTATIONS_OUTPUT_FILENAME, "w") as f:
        for name in names:
            f.write(salutation(greeting, name))
            f.write("\n")
    with open(SALUTATIONS_OUTPUT_FILENAME, "rb") as f:
        write_output_file(salutations_output_url, f)

    # It's polite to say goodbye!
    print(f"Goodbye!")
