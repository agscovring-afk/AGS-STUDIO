class WorkspaceManager:

    def __init__(self):

        self.open_pages = []

    def open(self, page):

        self.open_pages.append(page)

    def close(self, page):

        if page in self.open_pages:
            self.open_pages.remove(page)
