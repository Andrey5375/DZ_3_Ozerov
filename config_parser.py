import re
import json
import sys

class ConfigParser:
    def __init__(self, output_file=None):
        self.variables = {}
        self.output_file = output_file

    def transform_value(self, value):
        value = value.strip()
        if value.startswith('$') and value.endswith('$'):
            variable_name = value[1:-1].strip()
            if variable_name in self.variables:
                return self.variables[variable_name]
            else:
                raise ValueError(f"Константа '{variable_name}' не определена.")
        elif value.isdigit():
            return int(value)
        elif re.match(r'^\d+\.\d+$', value):
            return float(value)
        elif value.lower() == "true":
            return True
        elif value.lower() == "false":
            return False
        elif value.startswith('[') and value.endswith(']'):
            return self.parse_array(value[1:-1].strip())
        elif value.startswith('{') and value.endswith('}'):
            return self.parse_dict(value[1:-1].strip())
        else:
            return value.strip('"')

    def parse_array(self, value):
        items = value.split(';')
        return [self.transform_value(item.strip()) for item in items if item.strip()]

    def parse_dict(self, value):
        items = value.split(',')
        dictionary = {}
        for item in items:
            key_value_match = re.match(r'(\w+)\s*:\s*(.+)', item.strip())
            if key_value_match:
                key = key_value_match.group(1).strip()
                value = key_value_match.group(2).strip()
                dictionary[key] = self.transform_value(value)
            else:
                raise ValueError(f"Некорректный формат элемента словаря '{item.strip()}'.")
        return dictionary

    def handle_constant_declaration(self, lines):
        name = lines[0].split(':=')[0].strip()
        value_lines = lines[0].split(':=')[1:] + lines[1:]
        value = ' '.join(value_lines).strip()
        value = self.transform_value(value)
        self.variables[name] = value
        print(f"Добавлена константа: {name} = {value}")

    def parse(self, input_stream):
        lines = input_stream.readlines()
        in_multiline_comment = False
        buffer = []
        for line in lines:
            line = line.strip()

            if not line or line.startswith('#'):
                continue

            if line.startswith('=begin'):
                in_multiline_comment = True
                continue
            if line.startswith('=cut'):
                in_multiline_comment = False
                continue
            if in_multiline_comment:
                continue

            if ':=' in line:
                if buffer:
                    self.handle_constant_declaration(buffer)
                    buffer = []
                buffer.append(line)
            else:
                buffer.append(line)

        if buffer:
            self.handle_constant_declaration(buffer)

    def save_to_json(self, output):
        data = self.variables
        if isinstance(output, str):
            with open(output, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        else:
            json.dump(data, output, ensure_ascii=False, indent=4)

def main():
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else "output.json"

        with open(input_file, 'r', encoding='utf-8') as file:
            parser = ConfigParser(output_file)
            parser.parse(file)
            parser.save_to_json(output_file)
    else:
        print("Ошибка: Не указан файл входных данных или выходной файл.")

if __name__ == '__main__':
    main()
