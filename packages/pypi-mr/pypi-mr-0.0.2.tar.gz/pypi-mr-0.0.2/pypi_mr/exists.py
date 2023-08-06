import argparse
import os
from pathlib import Path
import requests
from pypi_mr.util import environ_or_required


def main(
    pypi_repository_url: str,
    pypi_username: str,
    pypi_password: str,
    package_dir: str = 'dist',
    fail_on_exists: bool = True,
) -> None:
    for file in Path(package_dir).iterdir():
        if requests.head(f'{pypi_repository_url}/packages/{file.name}', auth=(pypi_username, pypi_password)).ok:
            message = f'File {file.name} already exists on pypi'
            if fail_on_exists:
                raise FileExistsError(message)
            print(message)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--package-dir', type=str, default=os.environ.get('PACKAGE_DIR', 'dist'))
    parser.add_argument('--pypi-repository-url', type=str, **environ_or_required('PYPI_REPOSITORY_URL'))
    parser.add_argument('--pypi-username', type=str, **environ_or_required('PYPI_USERNAME'))
    parser.add_argument('--pypi-password', type=str, **environ_or_required('PYPI_PASSWORD'))
    parser.add_argument('--fail-on-exists', action=argparse.BooleanOptionalAction, default=True)
    parsed_args = parser.parse_args()
    main(**vars(parsed_args))
