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

    def walk_repository_and_collect_results(self, folder_path):
        results = []
        for root, _, files in os.walk(folder_path):
            for file_name in files:
                try:
                    file_path = os.path.join(root, file_name)
                    parsed_meta_data = code_parser_service.parse_file(file_path)
                    results.append(parsed_meta_data)
                except Exception as e:
                    print(str(e))
        return results


