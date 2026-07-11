class DragDropRuntime:

    def __init__(self):

        self.elements = []


    def move(self, element, position):

        self.elements.append({
            "element": element,
            "position": position
        })


        return self.elements
