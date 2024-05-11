from app.service.parser_service.core.parser_strategy import ParserStrategy


class PythonParserStrategy(ParserStrategy):
    def __init__(self, file_path):
        parser_lang = 'javascript'
        class_name_pattern = r'class\s+([A-Za-z_$][A-Za-z0-9_$]*)\s*[{]'
        super().__init__(file_path, parser_lang, class_name_pattern)

    def retrieve_function_metadata(self):
        metadata = []
        for node in self.tree.root_node.children:
            pass
            # class_name = self.get_class_name(node) if node.type == 'class_definition' else None
            # print(node.type)
            # self.extract_function_metadata(metadata, node, class_name)
        return metadata

    def extract_function_metadata(self, metadata, node, class_name=None):
        self.add_valid_metadata(metadata, node, class_name)

        for child in node.children:
            self.extract_function_metadata(metadata, child, class_name)

    def add_valid_metadata(self, metadata, node, class_name):
        # if 'definition' in node.type and node.type != 'class_definition':
        metadata.append({
            'function_type': node.type,
            'file_name': self.file_name,
            'file_extension': self.file_extension,
            'function_code': self.get_code_snippet(node),
            'function_name': 'askj',
            'class_name': class_name,
        })
