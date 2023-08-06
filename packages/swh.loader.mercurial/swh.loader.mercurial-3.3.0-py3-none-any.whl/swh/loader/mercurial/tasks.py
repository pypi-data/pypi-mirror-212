# Copyright (C) 2020-2023  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from celery import shared_task

from swh.loader.core.utils import parse_visit_date
from swh.loader.mercurial.directory import HgDirectoryLoader

from .loader import HgArchiveLoader, HgLoader


def _process_kwargs(kwargs):
    if "visit_date" in kwargs:
        kwargs["visit_date"] = parse_visit_date(kwargs["visit_date"])
    return kwargs


@shared_task(name=__name__ + ".LoadMercurial")
def load_hg(**kwargs):
    """Mercurial repository loading

    Import a mercurial tarball into swh.

    Args: see :func:`HgLoader` constructor.

    """
    loader = HgLoader.from_configfile(**_process_kwargs(kwargs))
    return loader.load()


@shared_task(name=__name__ + ".LoadArchiveMercurial")
def load_hg_from_archive(**kwargs):
    """Import a mercurial tarball into swh.

    Args: see :func:`HgArchiveLoader` constructor.
    """
    loader = HgArchiveLoader.from_configfile(**_process_kwargs(kwargs))
    return loader.load()


@shared_task(name=__name__ + ".LoadMercurialDirectory")
def load_hg_directory(**kwargs):
    """Import a mercurial tree into swh.

    Args: see :func:`HgDirectoryLoader` constructor.
    """
    loader = HgDirectoryLoader.from_configfile(**_process_kwargs(kwargs))
    return loader.load()
