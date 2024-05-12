from git import Repo
from app.utils.general import get_folder_from_temp_data_directory
import os
from app.service.parser_service.parser_service import CodeParserService

code_parser_service = CodeParserService()

class RepositoryService:

    def clone_local(self, url, folder_name):
        folder_path = get_folder_from_temp_data_directory(folder_name)
        cloned_repo = Repo.clone_from(url, folder_path)
        return cloned_repo

    def walk_repository_and_collect_results(self):
        folder_path = '/Users/yashsharma/Desktop/yash/odin/temp_data/AOecRto80EhKKfFQRFnXOQ1xgd82-1715463366811'
        file_name = "/Users/yashsharma/Desktop/yash/odin/temp_data/mine.js"
        return code_parser_service.parse_file(file_name)
        # for root, _, files in os.walk(folder_path):
        #     for file_name in files:
        #         file_path = os.path.join(root, file_name)
        #         code_parser_service.parse_file()
        #         print(file_path)
                # process_file(file_path)

