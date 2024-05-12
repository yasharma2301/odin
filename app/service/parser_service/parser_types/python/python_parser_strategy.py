from app.service.parser_service.core.parser_strategy import ParserStrategy


class PythonParserStrategy(ParserStrategy):
    def __init__(self, file_path):
        parser_lang = 'python'
        class_name_pattern = (r"(?:abstract\s+)?class\s+([A-Za-z_][A-Za-z0-9_]*)\s*(?:\(\s*([A-Za-z_]["
                              r"A-Za-z0-9_]*)\s*\))?\s*:")
        function_name_pattern = r"def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\("
        super().__init__(file_path, parser_lang, class_name_pattern, function_name_pattern)

    def retrieve_function_metadata(self):
        metadata = []
        self.extract_function_metadata(metadata, self.tree.root_node)
        return metadata

    def extract_function_metadata(self, metadata, node, class_name=None):
        if node.type == 'class_definition':
            class_name = self.get_class_name(node)
        self.add_valid_metadata(metadata, node, class_name)

        for child in node.children:
            self.extract_function_metadata(metadata, child, class_name)

    def add_valid_metadata(self, metadata, node, class_name=None):
        if 'definition' in node.type and node.type != 'class_definition':
            metadata.append({
                'function_type': node.type,
                'file_name': self.file_name,
                'file_extension': self.file_extension,
                'function_code': self.get_code_snippet(node),
                'function_name': self.get_function_name(node),
                'class_name': class_name,
            })
