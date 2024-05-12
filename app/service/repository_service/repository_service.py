from git import Repo
from app.utils.general import get_folder_from_temp_data_directory
import os
from app.service.parser_service.parser_service import CodeParserService
from app.utils.custom_logger import logger

code_parser_service = CodeParserService()


class RepositoryService:

    def clone_local(self, url, folder_name):
        folder_path = get_folder_from_temp_data_directory(folder_name)
        cloned_repo = Repo.clone_from(url, folder_path)
        return cloned_repo

    def walk_repository_and_collect_results(self, folder_name):
        log_prefix = "RepositoryService::walk_repository_and_collect_results:"
        folder_path = get_folder_from_temp_data_directory(folder_name)
        results = []

        def process_directory(folder_path):
            for root, _, files in os.walk(folder_path):
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    file, file_extension = os.path.splitext(file_path)
                    base_result_object = {
                        'file_name': file_name,
                        'file_extension': file_name.replace(file_extension, ''),
                        'parent_folder_path': root.replace(folder_path, ''),
                    }
                    try:
                        parsed_meta_data = code_parser_service.parse_file(file_path)
                        results.append({
                            **base_result_object,
                            'metadata_list': parsed_meta_data,
                            'status': 'SUCCESS',
                        })
                    except Exception as e:
                        logger.error(f"{log_prefix} {str(e)}")
                        results.append({
                            **base_result_object,
                            'status': 'FAILED',
                            'error': str(e)
                        })
                for directory in os.listdir(root):
                    full_path = os.path.join(root, directory)
                    if os.path.isdir(full_path):
                        process_directory(full_path)

        process_directory(folder_path)
        return results

    def clean_folder_if_exists(self, folder_name):
        folder_path = get_folder_from_temp_data_directory(folder_name)
        if os.path.exists(folder_path):
            os.system(f"rm -rf {folder_path}")
        return True

