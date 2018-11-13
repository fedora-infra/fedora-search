import logging
import re
from concurrent.futures import ThreadPoolExecutor

import django
import requests
from tenacity import retry, stop_after_attempt

django.setup()

from fedsearch.pkgsearch.models import Package  # NOQA

LOGGER = logging.getLogger(__name__)

PACKAGE_LIST_URL = "https://src.fedoraproject.org/extras/pagure_poc.json"

SESSION = requests.Session()


def get_package_list():
    """ Gather the list of rpms from src.fp.o """
    response = SESSION.get(PACKAGE_LIST_URL)
    if response.ok:
        packages = response.json().get("rpms")
        return packages


def get_last_active_branch(package):
    """ Return the latest active branch for a package """
    response = SESSION.get(f"https://src.fedoraproject.org/api/0/rpms/{package}/git/branches")
    if response.ok:
        results = response.json().get("branches")
        branches = []
        for branch in results:
            if re.match(r"^f\d+$", branch):
                branches.append(int(branch.strip("f")))

        if branches:
            return max(branches)

    print(f"No branch found for {package}")


@retry(stop=stop_after_attempt(5))
def get_package_data(package):
    """ Gather data from a package using mdapi """
    branch = get_last_active_branch(package)
    if branch is not None:
        response = SESSION.get(f"https://apps.fedoraproject.org/mdapi/f{branch}/srcpkg/{package}")
        if response.ok:
            data = response.json()
            data["name"] = package
            return data
        print(f"No mdapi info found for {package}")


if __name__ == "__main__":

    packages = get_package_list()

    with ThreadPoolExecutor(max_workers=40) as executor:
        for pkg_data in executor.map(get_package_data, packages):
            if pkg_data is not None:
                print(f"Indexing {pkg_data['name']}")
                Package.objects.create(
                    name=pkg_data["name"],
                    summary=pkg_data.get("summary"),
                    description=pkg_data.get("description"),
                    point_of_contact="",
                    icon="",
                    upstream_url=pkg_data.get("url"),
                )
