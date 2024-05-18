from src.assembler.assemblerisc import assemble
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-x", "--hex", help="Output in hex.", action="store_true")
    args = parser.parse_args()
    as_hex = args.hex

    binary_code, hex_code = assemble("../examples/tryouts.s")

    with open("../output/out_binary.txt", 'w') as out_binary_file:
        out_binary_file.write(binary_code)
    with open("../output/out_hexadeciaml.txt", 'w') as out_hex_file:
        out_hex_file.write(hex_code)


if __name__ == "__main__":
    main()
