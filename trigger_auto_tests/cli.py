import sys
from pathlib import Path

import click

from trigger_auto_tests.main import main
from trigger_auto_tests.utils.cli_helpers import PathPath


@click.command(
    help="Trigger Automated Tests on TeamCity for specified Shells and changed package"
)
@click.option(
    "--supported-shells", required=True, help='Specify as Shell names divided by ";"',
)
@click.option(
    "--automation-project-id", required=True, help="Project id for the Automated tests",
)
@click.option("--package-name", required=True, help="Updated package name")
@click.option(
    "--package-path",
    required=True,
    type=PathPath(exists=True, file_okay=False),
    help="Path to the updated package",
)
@click.option(
    "--package-vcs-url", required=True, help="URL of the updated package VCS",
)
@click.option(
    "--package-commit-id",
    required=True,
    help="Commit id of the updated package that would be used",
)
@click.option("--tc-url", required=True, help="TeamCity URL")
@click.option("--tc-user", required=True, help="TeamCity User")
@click.option("--tc-password", required=True, help="TeamCity Password")
def cli(
    supported_shells: str,
    automation_project_id: str,
    package_name: str,
    package_path: Path,
    package_vcs_url: str,
    package_commit_id: str,
    tc_url: str,
    tc_user: str,
    tc_password: str,
) -> bool:
    supported_shells = list(map(str.strip, supported_shells.split(";")))
    is_success = main(
        supported_shells=supported_shells,
        automation_project_id=automation_project_id,
        package_name=package_name,
        package_path=package_path,
        package_vcs_url=package_vcs_url,
        package_commit_id=package_commit_id,
        tc_url=tc_url,
        tc_user=tc_user,
        tc_password=tc_password,
    )
    if not is_success:
        sys.exit(1)
    return is_success


if __name__ == "__main__":
    cli()
