from abc import ABC, abstractmethod
import tree_sitter_languages as tree_sitter
import os
import re

class ParserStrategy(ABC):
    def __init__(self, file_path, parser_lang, class_name_pattern):
        self.file_path = file_path
        self.parser_lang = parser_lang
        self.class_name_pattern = class_name_pattern
        self.file_name, self.file_extension = self.__set_file_name()
        self.source_code = self.__read_source_code()
        self.parser = self.__set_parser()
        self.tree = self.__set_tree()

    def __read_source_code(self):
        try:
            with open(self.file_path, 'r') as file:
                source_code = file.read()
            return source_code
        except Exception as e:
            raise Exception(f"Failed to read source code for file {self.file_path} error: {str(e)}")

    def __set_parser(self):
        return tree_sitter.get_parser(self.parser_lang)

    def __set_tree(self):
        return self.parser.parse(bytes(self.source_code, 'utf8'))

    def __set_file_name(self):
        directory, file_name = os.path.split(self.file_path)
        file_name_without_ext, file_extension = os.path.splitext(file_name)
        return file_name_without_ext, file_extension

    @abstractmethod
    def retrieve_function_metadata(self):
        pass

    def get_code_snippet(self, node):
        return self.source_code[node.start_byte:node.end_byte]

    def get_class_name(self, node):
        class_code = self.get_code_snippet(node)
        match = re.search(self.class_name_pattern, class_code)
        if match:
            return match.group(1)
        return None
