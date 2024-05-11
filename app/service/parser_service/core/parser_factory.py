from app.service.parser_service.parser_types.js.js_parser_strategy import JsParserStrategy
from app.service.parser_service.parser_types.python.python_parser_strategy import PythonParserStrategy
import os


class ParserFactory:
    @classmethod
    def get_dedicated_parser(cls, file_path):
        extension_type = os.path.splitext(file_path)[1]
        match extension_type:
            case '.js':
                return JsParserStrategy(file_path)
            case '.py':
                return PythonParserStrategy(file_path)
            case _:
                raise Exception(f"Unhandled extension type of file {extension_type}")
