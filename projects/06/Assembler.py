import argparse
import os

from SymbolTable import SymbolTable
import Parser
import Coder

class Assembler(object):
    def __init__(self, parser, coder):
        self.symbol_table = SymbolTable()
        self.parser = parser
        self.coder = coder

    def assemble(self, file_name):
        file_asm = open(file_name + '.asm', 'r')
        file_hack = open(file_name + '.hack', 'w')
        line_number = 0
        for line in file_asm:
            # First pass - Symbols
            line = self.parser.strip_whitespace_and_comments(line)
            if line == '' or line.startswith('//'):
                continue
            if line.startswith('(') and line.endswith(')'):
                # Label
                label = line[1:-1]
                self.symbol_table.add_label(label, line_number)
                continue
            line_number += 1
        # Reset file cursor
        file_asm.seek(0)
        for line in file_asm:
            # Second pass - Parse commands
            line = self.parser.strip_whitespace_and_comments(line)
            if line == '' or line.startswith('//'):
                continue
            if line.startswith('(') and line.endswith(')'):
                continue
            write_line = ''
            if line.startswith('@'):
                # A-command
                try:
                    address = int(line[1:])
                except ValueError:
                    address = self.symbol_table.get_variable(line[1:])
                finally:
                    write_line = self.coder.int_to_bin_16(address)
            else:
                # C-command
                d, c, j = self.parser.parse(line)
                write_line = '111' + self.coder.comp(c) + self.coder.dest(d) + self.coder.jump(j)
            file_hack.write(write_line + '\n')
        file_asm.close()
        file_hack.close()

def main():
    args = parse_args()
    file_name, file_extension = os.path.splitext(args.file_path)
    if not os.path.exists(args.file_path):
        raise Exception('Invalid file or directory')
    if file_extension != '.asm':
        raise Exception('Invalid file extension')
    Assembler(Parser, Coder).assemble(file_name)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', help='Hack assembly language file to be converted to binary code')
    return parser.parse_args()

if __name__ == "__main__": main()
