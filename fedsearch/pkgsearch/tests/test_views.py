from mixer.backend.django import mixer
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from fedsearch.pkgsearch.models import Package
from fedsearch.pkgsearch.tests.utils import create_pkgs


class PackageViewTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        create_pkgs()

    def test_search_package_name(self):
        url = reverse("search")
        response = self.client.get(url, {"q": "gnome-terminal"})
        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]["name"] == "gnome-terminal"

    def test_search_package_summary(self):
        url = reverse("search")
        response = self.client.get(url, {"q": "terminal"})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3
        assert response.data[0]["name"] == "mate-terminal"
        assert response.data[1]["name"] == "gnome-terminal"
        assert response.data[2]["name"] == "tmux"
