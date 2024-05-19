from assembler.assemblerisc import assemble
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Input assembly file name.")
    args = parser.parse_args()
    input_file = args.input if args.input else '../examples/tryouts.s'

    binary_code, hex_code = assemble(input_file)

    with open("../output/out_binary.txt", 'w') as out_binary_file:
        out_binary_file.write(binary_code)
    with open("../output/out_hexadeciaml.txt", 'w') as out_hex_file:
        out_hex_file.write(hex_code)


if __name__ == "__main__":
    main()
