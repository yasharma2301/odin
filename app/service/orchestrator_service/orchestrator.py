from app.service.repository_service.repository_service import RepositoryService
from app.utils.general import current_milli_time
repository_service = RepositoryService()
from app.core.setup_sql import get_db
from app.repository.repository_repo.repository_repo import RepositoryRepo
from app.utils.custom_logger import logger


class Orchestrator:

    def __init__(self):
        self.db = next(get_db())
        self.repository_repo = RepositoryRepo(self.db)

    def run(self, repo_request):
        run_status = True
        repo_database_id = repo_request['id']
        url = repo_request['url']
        folder_name = f"{repo_request['user_id']}-{current_milli_time()}"

        try:
            # Step 1: Make sure there is corresponding entry in database
            # repository_entry = self.repository_repo.get_repository_by_id(repo_database_id)
            # assert repository_entry is not None
            # assert repository_entry.status == 'QUEUED'
            #
            # # Step 2: Mark the repository as processing
            # repository_entry = self.repository_repo.update_repository(repo_database_id, {'status': 'IN_PROGRESS'})
            # assert repository_entry is not None
            # assert repository_entry.status == 'IN_PROGRESS'

            # Step 3: Clone the repository and walk through the files
            repository_service.clone_local(url, folder_name)

            # Step 4: Walk through the repository and collect the results
            results = repository_service.walk_repository_and_collect_results(folder_name)

            # Step 5: Store the results in the database
            print(results)
        except Exception as e:
            logger.error(f"Orchestrator::run: {str(e)}")
            try:
                self.repository_repo.update_repository(repo_database_id, {'status': 'FAILED'})
            except Exception as e:
                logger.error(f"Orchestrator::run:error: {str(e)}")
            run_status = False
        finally:
            # Step 5: Cleanup the cloned folder if any
            repository_service.clean_folder_if_exists(folder_name)

        return run_status

