import re

from queue import Queue
from threading import Thread

import requests

from django.core.management.base import BaseCommand
from django.contrib.postgres.search import SearchVector
from fedsearch.pkgsearch.models import Package, SubPackage  # NOQA


class Command(BaseCommand):
    help = "Index the list of packages and subpackages"

    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(max_retries=20)
    session.mount("https://", adapter)

    packages = (
        session.get("https://src.fedoraproject.org/extras/pagure_poc.json").json().get("rpms")
    )

    Q = Queue()

    def call_api(self, url):
        data = {}
        response = self.session.get(url)
        if response.ok:
            data = response.json()

        return data

    def get_last_active_branch(self, package):
        """ Return the latest active branch for a package """
        data = self.call_api(f"https://src.fedoraproject.org/api/0/rpms/{package}/git/branches")
        results = data.get("branches")
        if results:
            branches = []
            for branch in results:
                if re.match(r"^f\d+$", branch):
                    branches.append(int(branch.strip("f")))

            if branches:
                return max(branches)

        print(f"No branch found for {package}")

    def index_packages(self):
        """ Gather data from a package using mdapi """
        while True:
            package = self.Q.get()

            if type(package) is tuple:

                pkg, branch, parrent = package
                data = self.call_api(f"https://apps.fedoraproject.org/mdapi/f{branch}/pkg/{pkg}")
                self.stdout.write(self.style.SUCCESS(f"Indexing Subpackage {pkg}"))
                parrent.subpkgs.create(
                    name=pkg, summary=data.get("summary"), description=data.get("description")
                )
                self.Q.task_done()

            else:

                branch = self.get_last_active_branch(package)
                if branch is not None:
                    data = self.call_api(
                        f"https://apps.fedoraproject.org/mdapi/f{branch}/srcpkg/{package}"
                    )

                    if data:
                        self.stdout.write(self.style.SUCCESS(f"Indexing {package}"))
                        package_obj = Package.objects.create(
                            name=data["basename"],
                            summary=data.get("summary"),
                            description=data.get("description"),
                            point_of_contact=self.packages.get(data["basename"]),
                            icon="",
                            upstream_url=data.get("url"),
                        )

                        package_obj.search_vector = (
                            SearchVector("name", weight="A", config="english")
                            + SearchVector("summary", weight="B", config="english")
                            + SearchVector("description", weight="D", config="english")
                        )
                        package_obj.save()

                        for pkg in data.get("co-packages", []):
                            if pkg != package:
                                data = (pkg, branch, package_obj)
                                self.Q.put(data)

                        self.Q.task_done()

    def handle(self, *args, **options):

        for i in range(40):
            worker = Thread(target=self.index_packages)
            worker.setDaemon(True)
            worker.start()

        for package in self.packages:
            self.Q.put(package)

        self.Q.join()
