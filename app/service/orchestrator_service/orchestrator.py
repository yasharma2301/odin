from app.service.repository_service.repository_service import RepositoryService
from app.utils.general import current_milli_time

repository_service = RepositoryService()
from app.repository.repository_repo.repository_repo import RepositoryRepo
from app.utils.custom_logger import logger
from app.repository.file_repo.file_repo import FileRepo


class Orchestrator:

    def __init__(self):
        self.repository_repo = RepositoryRepo()
        self.file_repo = FileRepo()

    def run(self, repo_request):
        run_status = True
        repo_database_id = repo_request['id']
        url = repo_request['url']
        folder_name = f"{repo_request['user_id']}-{current_milli_time()}"

        try:
            # Step 1: Make sure there is corresponding entry in database
            repository_entry = self.repository_repo.get_repository_by_id(repo_database_id)
            assert repository_entry is not None
            assert repository_entry.status == 'QUEUED'

            # Step 2: Mark the repository as processing
            repository_entry = self.repository_repo.update_repository(repo_database_id, {'status': 'IN_PROGRESS'})
            assert repository_entry is not None
            assert repository_entry.status == 'IN_PROGRESS'

            # Step 3: Clone the repository and walk through the files
            repository_service.clone_local(url, folder_name)

            # Step 4: Walk through the repository and collect the results
            results = repository_service.walk_repository_and_collect_results(folder_name)

            # Step 5: Store the results in the database
            self.store_results(repo_database_id, results)

            # Step 6: Mark this job as success
            self.repository_repo.update_repository(repo_database_id, {'status': 'COMPLETED'})
        except Exception as e:
            logger.error(f"Orchestrator::run: {str(e)}")
            try:
                self.repository_repo.update_repository(repo_database_id, {'status': 'FAILED', 'error': str(e)})
            except Exception as e:
                logger.error(f"Orchestrator::run:error: {str(e)}")
            run_status = False
        finally:
            # Cleanup the cloned folder if any
            repository_service.clean_folder_if_exists(folder_name)

        return run_status

    def store_results(self, repo_database_id, results):
        files_to_create = []

        for result in results:
            metadata_object = []
            if 'metadata_list' in result:
                for metadata in result['metadata_list']:
                    metadata_object.append({
                        'function_name': metadata['function_name'],
                        'function_code': metadata['function_code'],
                        'function_type': metadata['function_type'],
                        'class_name': metadata['class_name'],
                    })

            file_data = {
                'repository_id': repo_database_id,
                'file_extension': result['file_extension'],
                'file_name': result['file_name'],
                'parent_folder_path': result['parent_folder_path'],
                'status': result['status'],
                'error': None if 'error' not in result else result['error'],
                'metadata': metadata_object
            }
            files_to_create.append(file_data)

        return self.file_repo.create_files(files_to_create)
