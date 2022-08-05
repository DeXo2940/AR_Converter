import sys
import ar_converter_engine


def main(input_file_path, output_file_path):
    ar_converter_engine.convert(input_file_path, output_file_path)


if __name__ == '__main__':
    input_file_path = sys.argv[1] if len(
        sys.argv) >= 2 else input('Input file path: ')
    output_file_name = sys.argv[2] if len(
        sys.argv) >= 3 else input('Output file name: ')

    output_file_path = output_file_name if '.xlsx' in output_file_name else output_file_name + '.xlsx'

    print('Input: {}'.format(input_file_path))
    print('Output: {}'.format(output_file_path))

    main(input_file_path, output_file_path)
