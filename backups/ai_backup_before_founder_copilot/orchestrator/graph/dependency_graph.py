from collections import defaultdict


class DependencyGraph:

    def __init__(self):

        self.nodes = set()

        self.edges = defaultdict(list)


    def add_node(self, node):

        self.nodes.add(node)


    def add_dependency(self, node, depends_on):

        self.add_node(node)

        self.add_node(depends_on)

        self.edges[depends_on].append(node)


    def get_dependencies(self, node):

        result = []

        for parent, children in self.edges.items():

            if node in children:

                result.append(parent)

        return result


    def get_dependents(self, node):

        return self.edges.get(
            node,
            []
        )


    def can_execute(self, node, completed):

        dependencies = self.get_dependencies(
            node
        )

        return all(
            item in completed
            for item in dependencies
        )


    def topological_sort(self):

        visited = set()

        result = []


        def visit(node):

            if node in visited:

                return

            visited.add(node)


            for dep in self.get_dependencies(node):

                visit(dep)


            result.append(node)


        for node in self.nodes:

            visit(node)


        return result


    def clear(self):

        self.nodes.clear()

        self.edges.clear()


    def to_dict(self):

        return {

            "nodes": list(self.nodes),

            "edges": dict(self.edges)

        }