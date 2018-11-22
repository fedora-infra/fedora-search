from fedsearch.pkgsearch.models import Package
from django.contrib.postgres.search import SearchVector

search_vector = (
    SearchVector("name", weight="A", config="english")
    + SearchVector("summary", weight="B", config="english")
    + SearchVector("description", weight="D", config="english")
)


def create_pkgs():
    """ Helper method used to create instances of Package and SubPackage objects """
    package1, created = Package.objects.get_or_create(
        name="mate-terminal",
        summary="Terminal emulator for MATE",
        description="Mate-terminal is a terminal emulator for MATE. \
        It supports translucent backgrounds, opening multiple terminals \
        in a single window (tabs) and clickable URLs.",
        point_of_contact="asterix",
        icon="",
        upstream_url="http://mate-desktop.org/",
        search_vector=None,
    )
    package2, created = Package.objects.get_or_create(
        name="gnome-terminal",
        summary="Terminal emulator for GNOME",
        description="gnome-terminal is a terminal emulator for GNOME. \
        It features the ability to use multiple terminals in a single window (tabs) \
        and profiles support.",
        point_of_contact="obelix",
        icon="",
        upstream_url="http://www.gnome.org/",
        search_vector=None,
    )
    package3, created = Package.objects.get_or_create(
        name="tmux",
        summary="A terminal multiplexer",
        description='tmux is a "terminal multiplexer." It enables a number of terminals \
        (or windows) to be accessed and controlled from a single terminal. tmux is intended \
        to be a simple, modern, BSD-licensed alternative to programs such as GNU Screen.',
        point_of_contact="idefix",
        icon="",
        upstream_url="https://tmux.github.io/",
        search_vector=None,
    )

    package1.search_vector = search_vector
    package2.search_vector = search_vector
    package3.search_vector = search_vector

    package1.save()
    package2.save()
    package3.save()

    package2.subpkgs.create(
        name="gnome-terminal-nautilus",
        summary=" Subpackage of gnome-terminal ",
        description="GNOME Terminal extension for Nautilus",
    )
