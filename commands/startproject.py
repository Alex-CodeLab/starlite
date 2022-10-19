import os, re, io, httpx, zipfile
from typing import TYPE_CHECKING
from urllib.parse import urlparse
import tempfile
from cleo import Command
from cleo.helpers import argument, option
import shutil

if TYPE_CHECKING:
    from starlite.app import Starlite


class StartProject(Command):
    """
    Create a new project

    startproject
        {--template= : How many times should the message be printed?}
    """
    name = "startproject"
    description = "Create a new project"

    TEMP_PROJECT_ZIP = os.path.join(tempfile.gettempdir(), 'starlite', 'project_template.zip')

    def handle(self) -> None:
        template = self.option('template')

        def local_zip(template_file):
            source = template_file or os.path.join(os.getcwd(), 'commands', 'templates', 'project_template.zip')
            shutil.copy(source, TEMP_PROJECT_ZIP)

        self.download(template) if self.is_url(template) else local_zip(self.option('template'))
        self.parse_template(template or TEMP_PROJECT_ZIP)

    def download(self, url):
        """
        Download the given URL (zip).
        """
        client = httpx.Client(timeout=20)
        response = client.get(url, follow_redirects=True)
        tempdir = os.path.join(tempfile.gettempdir(), 'starlite')
        if not os.path.exists(tempdir):
            os.makedirs(tempdir)
        with open(TEMP_PROJECT_ZIP, 'w+b') as f:
            f.write(response.content)

    def parse_template(self, template_zip):
        tmpdir = os.path.join(tempfile.gettempdir(), 'starlite')
        tempdir_extract = os.path.join(tmpdir, 'template_zip')
        if not os.path.exists(tempdir_extract):
            os.makedirs(tempdir_extract)

        with zipfile.ZipFile(template_zip, 'r') as zipObj:
            # Extract all the contents of zip file in different directory
            zipObj.extractall(tempdir_extract)

        # TODO: render the template files (Jinja / Mako) and copy them to the project-folder


    def is_url(self, template):
        """Return True if the name looks like a URL."""
        return bool(re.match("^(http|https):/", template)) if template else False
