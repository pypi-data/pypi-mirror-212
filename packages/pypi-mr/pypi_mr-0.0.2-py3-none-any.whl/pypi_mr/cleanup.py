import argparse
import typing as tp
import xml.etree.ElementTree as ET

import requests
from packaging.version import Version
from pypi_mr.util import environ_or_required


def pypi_mr_packages(
    package: str,
    pypi_host: str,
    pypi_user: str,
    pypi_password: str,
) -> tp.List[tp.Dict[str, tp.Any]]:
    text = requests.get(f'{pypi_host}/simple/{package}/', auth=(pypi_user, pypi_password)).text
    packages = []
    for _line in text.splitlines():
        if '<a href="/packages' not in _line:
            continue
        line = ET.fromstring(_line.removesuffix('<br>').strip()).text
        if not isinstance(line, str):
            raise Exception(f'Failed to parse line {line}')
        if line.endswith('.tar.gz'):
            ver = line.removesuffix('.tar.gz')
            pypi_name, version = ver.rsplit('-', maxsplit=1)
        if line.endswith('-py3-none-any.whl'):
            ver = line.removesuffix('-py3-none-any.whl')
            pypi_name, version = ver.rsplit('-', maxsplit=1)
        v = Version(version).release
        if len(v) == 4:  # major, minor, patch, mr  # noqa: PLR2004
            mr_id = v[-1]
            packages.append({'pypi_name': pypi_name, 'version': version, 'mr_id': mr_id})
    return packages


def pypi_remove_package(
    package: str,
    version: str,
    pypi_host: str,
    pypi_user: str,
    pypi_password: str,
) -> None:
    data = {':action': 'remove_pkg', 'name': package, 'version': version}
    r = requests.post(pypi_host, data=data, auth=(pypi_user, pypi_password))
    if not r.ok:
        raise Exception(f'Failed to remove package {package} {version} {r.status_code} {r.text}')


def main(
    gitlab_api_token: str,
    gitlab_api_url: str,
    project_id: str,
    pypi_package_name: str,
    pypi_repository_url: str,
    pypi_username: str,
    pypi_password: str,
    mr_states: tp.FrozenSet[str] = frozenset({'closed', 'merged'}),
) -> None:
    mr_ids = set()
    for state in mr_states:
        for mr in requests.get(
            f'{gitlab_api_url}/projects/{project_id}/merge_requests',
            params={'state': state},
            headers={'Authorization': f'Bearer {gitlab_api_token}'},
        ).json():
            mr_ids.add(mr['iid'])

    for package in pypi_mr_packages(pypi_package_name, pypi_repository_url, pypi_username, pypi_password):
        if package['mr_id'] in mr_ids:
            pypi_remove_package(package['pypi_name'], package['version'], pypi_repository_url, pypi_username, pypi_password)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--gitlab-api-token', type=str, **environ_or_required('GITLAB_API_TOKEN'))
    parser.add_argument('--gitlab-api-url', type=str, **environ_or_required('CI_API_V4_URL'))
    parser.add_argument('--project-id', type=str, **environ_or_required('CI_PROJECT_ID'))
    parser.add_argument('--pypi-package-name', type=str, **environ_or_required('PYPI_PACKAGE_NAME'))
    parser.add_argument('--pypi-repository-url', type=str, **environ_or_required('PYPI_REPOSITORY_URL'))
    parser.add_argument('--pypi-username', type=str, **environ_or_required('PYPI_USERNAME'))
    parser.add_argument('--pypi-password', type=str, **environ_or_required('PYPI_PASSWORD'))
    parsed_args = parser.parse_args()
    main(**vars(parsed_args))
