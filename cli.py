from pathlib import Path

import click

from main import main


@click.command(
    help='Trigger Automated Tests on TeamCity for specified Shells and changed package'
)
@click.option(
    '--supported-shells',
    required=True,
    help='Specify as Shell names divided by ";"',
)
@click.option(
    '--automation-project-name',  # fixme rename name to id
    required=True,
    help='Project id for the Automated tests',
)
@click.option('--package-name', required=True, help='Updated package name')
@click.option(
    '--package-path',
    required=True,
    type=click.Path(exists=True, file_okay=False),
    help='Path to the updated package',
)
@click.option(
    '--package-vcs-url',
    required=True,
    help='URL of the updated package VCS',
)
@click.option(
    '--package-commit-id',
    required=True,
    help='Commit id of the updated package that would be used',
)
@click.option('--tc-url', required=True, help='TeamCity URL')
@click.option('--tc-user', required=True, help='TeamCity User')
@click.option('--tc-password', required=True, help='TeamCity Password')
def cli(
        supported_shells: str,
        automation_project_name: str,
        package_name: str,
        package_path: Path,
        package_vcs_url: str,
        package_commit_id: str,
        tc_url: str,
        tc_user: str,
        tc_password: str,
) -> bool:
    supported_shells = supported_shells.split(';')
    package_path = package_path if isinstance(package_path, Path) else Path(package_path)
    is_success = main(
        supported_shells=supported_shells,
        automation_project_name=automation_project_name,
        package_name=package_name,
        package_path=package_path,
        package_vcs_url=package_vcs_url,
        package_commit_id=package_commit_id,
        tc_url=tc_url,
        tc_user=tc_user,
        tc_password=tc_password,
    )
    return is_success


if __name__ == '__main__':
    cli()
