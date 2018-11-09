from fedsearch.pkgsearch.models import Package


def create_pkgs():
    """ Helper method used to create instances of the Packages object """
    Package.objects.get_or_create(
        name="mate-terminal",
        summary="Terminal emulator for MATE",
        description="Mate-terminal is a terminal emulator for MATE. \
        It supports translucent backgrounds, opening multiple terminals \
        in a single window (tabs) and clickable URLs.",
        point_of_contact="asterix",
        icon="",
        upstream_url="http://mate-desktop.org/",
    )
    Package.objects.get_or_create(
        name="gnome-terminal",
        summary="Terminal emulator for GNOME",
        description="gnome-terminal is a terminal emulator for GNOME. \
        It features the ability to use multiple terminals in a single window (tabs) \
        and profiles support.",
        point_of_contact="obelix",
        icon="",
        upstream_url="http://www.gnome.org/",
    )
    Package.objects.get_or_create(
        name="tmux",
        summary="A terminal multiplexer",
        description='tmux is a "terminal multiplexer." It enables a number of terminals \
        (or windows) to be accessed and controlled from a single terminal. tmux is intended \
        to be a simple, modern, BSD-licensed alternative to programs such as GNU Screen.',
        point_of_contact="idefix",
        icon="",
        upstream_url="https://tmux.github.io/",
    )
