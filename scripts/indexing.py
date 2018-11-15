import logging
import re
from concurrent.futures import ThreadPoolExecutor

import django
import requests
from tenacity import retry, stop_after_attempt

django.setup()

from fedsearch.pkgsearch.models import Package, SubPackage  # NOQA

LOGGER = logging.getLogger(__name__)

PACKAGE_LIST_URL = "https://src.fedoraproject.org/extras/pagure_poc.json"

SESSION = requests.Session()


def call_api(url):
    data = {}
    response = SESSION.get(url)
    if response.ok:
        data = response.json()

    return data


def get_package_list():
    """ Gather the list of rpms from src.fp.o """
    data = call_api(PACKAGE_LIST_URL)
    return data.get("rpms")


def get_last_active_branch(package):
    """ Return the latest active branch for a package """
    data = call_api(f"https://src.fedoraproject.org/api/0/rpms/{package}/git/branches")
    results = data.get("branches")
    branches = []
    for branch in results:
        if re.match(r"^f\d+$", branch):
            branches.append(int(branch.strip("f")))

    if branches:
        return max(branches)

    print(f"No branch found for {package}")


def get_sub_packages(packages, branch):
    """ Returns a list of Subpackage objects """
    subpkgs = []
    for pkg in packages:
        data = call_api(f"https://apps.fedoraproject.org/mdapi/f{branch}/pkg/{pkg}")
        subpkgs.append(
            SubPackage(name=pkg, summary=data.get("summary"), description=data.get("description"))
        )
    return subpkgs


@retry(stop=stop_after_attempt(5))
def get_package_data(package):
    """ Gather data from a package using mdapi """
    branch = get_last_active_branch(package)
    if branch is not None:
        data = call_api(f"https://apps.fedoraproject.org/mdapi/f{branch}/srcpkg/{package}")

        if data.get("co-packages"):
            subpkgs = get_sub_packages(data.get("co-packages"), branch)
            data["subpackages"] = subpkgs

        return data

        print(f"No mdapi info found for {package}")


if __name__ == "__main__":

    packages = get_package_list()

    with ThreadPoolExecutor(max_workers=40) as executor:
        for pkg_data in executor.map(get_package_data, packages):
            if pkg_data:
                print(f"Indexing {pkg_data['basename']}")

                package = Package.objects.create(
                    name=pkg_data["basename"],
                    summary=pkg_data.get("summary"),
                    description=pkg_data.get("description"),
                    point_of_contact=packages.get(pkg_data["basename"]),
                    icon="",
                    upstream_url=pkg_data.get("url"),
                )

                for pkg in pkg_data.get("subpackages"):
                    pkg.package = package
                    pkg.save()
