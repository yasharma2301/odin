from app.service.parser_service.core.parser_factory import ParserFactory


class CodeParserService:

    @classmethod
    def parse_file(cls, file_path):
        parser = ParserFactory.get_dedicated_parser(file_path)
        return parser.retrieve_function_metadata()
