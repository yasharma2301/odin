from app.service.parser_service.core.parser_strategy import ParserStrategy
import re


class JsParserStrategy(ParserStrategy):
    def __init__(self, file_path):
        parser_lang = 'javascript'
        class_name_pattern = r'class\s+([A-Za-z_$][A-Za-z0-9_$]*)\s*[{]'
        function_name_pattern = r'function\s+([A-Za-z_$][A-Za-z0-9_$]*)\s*\('
        super().__init__(file_path, parser_lang, class_name_pattern, function_name_pattern)

    def retrieve_function_metadata(self):
        metadata = []
        for node in self.tree.root_node.children:
            class_name = self.get_class_name(node) if node.type == 'class_declaration' else None
            self.extract_function_metadata(metadata, node, class_name)
        return metadata

    def extract_function_metadata(self, metadata, node, class_name=None):
        self.add_valid_metadata(metadata, node, class_name)

        for child in node.children:
            self.extract_function_metadata(metadata, child, class_name)

    def add_valid_metadata(self, metadata, node, class_name):
        if 'function' in node.type or node.type == 'method_definition':
            code = self.get_code_snippet(node)
            if code != 'function':
                metadata.append({
                    'function_type': node.type,
                    'file_name': self.file_name,
                    'file_extension': self.file_extension,
                    'function_code': code,
                    'function_name': self.get_function_name(node),
                    'class_name': class_name,
                })

    def get_function_name(self, node):
        if node.type != 'function_declaration':
            return None
        super().get_function_name(node)
