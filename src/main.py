from assembler.assemblerisc import assemble
import argparse


def get_args() -> str:
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Input assembly file name.")
    args = parser.parse_args()
    input_file = args.input if args.input else '../examples/tryouts.s'
    return input_file


def write_output_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)


def main():
    input_filename = get_args()

    binary_code, hex_code = assemble(input_filename)

    write_output_file('../output/out_binary.txt', binary_code)
    write_output_file('../output/out_hexadeciaml.txt', hex_code)


if __name__ == "__main__":
    main()
