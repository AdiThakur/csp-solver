import sys


def main(input_filename: str, output_filename: str) -> None:
    pass


if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Usage: python3 battle.py <input_file> <output_file>")
        exit()
    
    main(
        input_filename=sys.argv[1],
        output_filename=sys.argv[2]
    )