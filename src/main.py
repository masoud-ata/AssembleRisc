import argparse
import glob

from assembler.assemblerisc import AssembleRisc


def run_regression() -> None:
    assembler = AssembleRisc()
    assembly_filenames = glob.glob("../regression/*.s")
    for assembly_filename in assembly_filenames:
        hex_code = _convert_to_hex(assembler.assemble(assembly_filename))
        golden_filename = assembly_filename.replace(".s", ".txt")
        with open(golden_filename, 'r') as golden_file:
            data = golden_file.read()
            if data != hex_code:
                print(f'{assembly_filename} failed!')


def get_args():
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("-i", "--input", help="Input assembly file name.")
    argument_parser.add_argument("-r", "--regression", action='store_true')

    args = argument_parser.parse_args()
    return args


def write_output_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)


def _convert_to_hex(binary_code) -> str:
    hex_result = ""
    codes = binary_code.splitlines()
    for code in codes:
        is_compressed = len(code) == 16
        if is_compressed:
            hex_result += '{0:04x}'.format(int(code, 2)) + "\n"
        else:
            hex_result += '{0:08x}'.format(int(code, 2)) + "\n"
    return hex_result


def _dump_bytes(hex_code) -> str:
    hex_result = ""
    codes = hex_code.splitlines()
    for code in codes:
        hex_result += code[::-1]
    return hex_result


def main():
    try:
        args = get_args()

        if args.regression:
            run_regression()

        input_filename = args.input if args.input else '../examples/tryouts.s'

        assembler = AssembleRisc()
        binary_code = assembler.assemble(input_filename)

        hex_code = _convert_to_hex(binary_code)
        hex_byte_dump = _dump_bytes(hex_code)

        write_output_file('../output/out_binary.txt', binary_code)
        write_output_file('../output/out_hexadeciaml.txt', hex_code)
        write_output_file('../output/out_byte_dump_hexadeciaml.txt', hex_byte_dump)
    except Exception as e:
        print(str(e))


if __name__ == "__main__":
    main()
