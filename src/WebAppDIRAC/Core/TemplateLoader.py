import os
from tornado.template import BaseLoader, Template


class TemplateLoader(BaseLoader):
    def __init__(self, pathList, **kwargs):
        super().__init__(**kwargs)
        self.pathList = pathList

    def resolve_path(self, name, parent_path=None):
        if parent_path and not parent_path.startswith("<"):
            if not parent_path.startswith("/") and not name.startswith("/"):
                name = os.path.join(os.path.dirname(parent_path), name)
        return name

    def _create_template(self, name):
        for path in self.pathList:
            try:
                f = open(os.path.abspath(os.path.join(path, name)), "rb")
            except OSError:
                continue
            template = Template(f.read(), name=name, loader=self)
            f.close()
            return template
        raise RuntimeError("Can't find template %s" % name)
