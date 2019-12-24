import time
from pathlib import Path
from typing import List

from github import Github
from github.Repository import Repository

from tc_api import TeamCityAPI
from pip_download import pip_download


REPOS_OWNER = 'QualiSystems'
BUILDS_CHECK_DELAY = 30


def get_file_content_from_github(repo_name: str, file_path: str) -> str:
    repo: Repository = Github().get_repo(f'{REPOS_OWNER}/{repo_name}')
    return repo.get_contents(file_path, 'master').decoded_content.decode()


def get_package_version(package_path: Path) -> str:
    with package_path.joinpath('version.txt').open() as fo:
        return fo.read().strip()


def is_package_in_requirements(
        requirements: str, package_name: str, package_version: str
) -> bool:
    conf = pip_download.PipDownloaderConfig()
    pip_downloader = pip_download.PipDownloader(conf)
    install_requirements = pip_downloader.parse_requirement_by_str(requirements)
    install_requirements = pip_downloader.resolve_range_dependencies(
        install_requirements
    )
    for install_requirement in install_requirements:
        if install_requirement.name == package_name:
            return install_requirement.specifier.contains(package_version)

    return False


def main(
        supported_shells: List[str],
        automation_project_name: str,
        package_name: str,
        package_path: Path,
        package_vcs_url: str,
        package_commit_id: str,
        tc_url: str,
        tc_user: str,
        tc_password: str,
):
    triggered_builds = {}
    builds_statuses = {}
    tc_api = TeamCityAPI(tc_url, tc_user, tc_password)

    for shell_name in supported_shells:
        requirements = get_file_content_from_github(
            shell_name, 'src/requirements.txt'
        )
        package_version = get_package_version(package_path)
        if is_package_in_requirements(requirements, package_name, package_version):
            print(f'{shell_name} Automation tests build triggering')
            build_queue_id = trigger_build(
                tc_api,
                shell_name,
                automation_project_name=automation_project_name,
                package_vcs_url=package_vcs_url,
                package_commit_id=package_commit_id,
            )
            triggered_builds[shell_name] = build_queue_id
        else:
            print(f'{shell_name} skipped tests')

    while triggered_builds:
        time.sleep(BUILDS_CHECK_DELAY)

        for shell_name, build_queue_id in triggered_builds.copy().items():
            data = tc_api.get_triggered_build_details(build_queue_id)
            if data.state == data.state.FINISHED:
                print(
                    f'{shell_name} Automation tests is finished '
                    f'with status {data.status.value}'
                )
                triggered_builds.pop(shell_name)
                builds_statuses[shell_name] = (data.status == data.status.SUCCESS)

    return all(builds_statuses.values())


def trigger_build(
        tc_api: TeamCityAPI,
        shell_name: str,
        automation_project_name: str,
        package_vcs_url: str,
        package_commit_id: str,
) -> int:
    locator_data = {
        # fixme remove _COPY
        'name': f'{shell_name}_COPY',
        'project': automation_project_name,
    }
    additional_data = {
        'triggeringOptions': {'queueAtTop': True},
        'properties': {'property': [
            {
                'name': 'conf.triggered_by_project.url',
                'value': package_vcs_url,
            },
            {
                'name': 'conf.triggered_by_project.commit_id',
                'value': package_commit_id,
            },
        ]}
    }
    data = tc_api.trigger_builds(locator_data, additional_data=additional_data)
    return data.id
