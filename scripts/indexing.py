import logging
import re

from queue import Queue
from threading import Thread

import django
import requests

django.setup()

from fedsearch.pkgsearch.models import Package, SubPackage  # NOQA

LOGGER = logging.getLogger(__name__)

PACKAGE_LIST_URL = "https://src.fedoraproject.org/extras/pagure_poc.json"

SESSION = requests.Session()
adapter = requests.adapters.HTTPAdapter(max_retries=20)
SESSION.mount("https://", adapter)

Q = Queue()


def call_api(url):
    data = {}
    response = SESSION.get(url)
    if response.ok:
        data = response.json()

    return data


def get_last_active_branch(package):
    """ Return the latest active branch for a package """
    data = call_api(f"https://src.fedoraproject.org/api/0/rpms/{package}/git/branches")
    results = data.get("branches")
    if results:
        branches = []
        for branch in results:
            if re.match(r"^f\d+$", branch):
                branches.append(int(branch.strip("f")))

        if branches:
            return max(branches)

    print(f"No branch found for {package}")


def index_packages():
    """ Gather data from a package using mdapi """
    while True:
        package = Q.get()

        if type(package) is tuple:

            pkg, branch, parrent = package
            data = call_api(f"https://apps.fedoraproject.org/mdapi/f{branch}/pkg/{pkg}")
            print(f"Indexing Subpackage {pkg}")
            parrent.subpkgs.create(
                name=pkg, summary=data.get("summary"), description=data.get("description")
            )
            Q.task_done()

        else:

            branch = get_last_active_branch(package)
            if branch is not None:
                data = call_api(f"https://apps.fedoraproject.org/mdapi/f{branch}/srcpkg/{package}")

                if data:
                    print(f"Indexing {package}")
                    package = Package.objects.create(
                        name=data["basename"],
                        summary=data.get("summary"),
                        description=data.get("description"),
                        point_of_contact=packages.get(data["basename"]),
                        icon="",
                        upstream_url=data.get("url"),
                    )

                    for pkg in data.get("co-packages", []):
                        if pkg != package:
                            data = (pkg, branch, package)
                            Q.put(data)

                    Q.task_done()


if __name__ == "__main__":

    packages = call_api(PACKAGE_LIST_URL).get("rpms")

    for i in range(40):
        worker = Thread(target=index_packages)
        worker.setDaemon(True)
        worker.start()

    for package in packages:
        Q.put(package)

    Q.join()
