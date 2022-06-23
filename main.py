from sys import argv

from ar_converter_engine import convert


def main(input_file_path, output_file_path):
    convert(input_file_path, output_file_path)


if __name__ == '__main__':
    input_file_path = argv[1] if len(argv) >= 2 else input('Input file path: ')
    output_file_name = argv[2] if len(argv) >= 3 else input('Output file name: ')

    output_file_path = output_file_name if '.xlsx' in output_file_name else output_file_name + '.xlsx'

    print('Input: ', input_file_path)
    print('Output: ', output_file_path)

    main(input_file_path, output_file_path)
