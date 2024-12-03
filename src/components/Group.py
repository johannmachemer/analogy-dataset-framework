from src.components.Component import *


class Group(Component):

    def __init__(self, component_identifier, superior_component= None, previous_version = None):
        """
        Instantiate a Single Image node.
        """
        self.components = []
        super().__init__(component_identifier, Type("Group"), superior_component, previous_version)
        # all children components

    def insert_component(self, node):
        """
        Insert a component to the Single Image node.
        """
        self.components.append(node)

    def calculate_bounding_box(self):
        for component in self.components:
            component.calculate_bounding_box()

    def sample(self, attr=None):
        """
        sample components of group (recursive)
        """
        super().sample(attr)
        self.sample_child_components(attr)

    def sample_child_components(self, attr=None):
        for component in self.components:
            component.sample(attr)

    def get_all_components(self):
        result = []
        for component in self.components:
            result.append(component)
            if isinstance(component, Group):
                result.extend(component.get_all_components())

        return result

    def get_component_by_identifier(self, component_identifier):
        if self.get_unique_component_identifier() == component_identifier:
            return self
        for component in self.components:
            if component.get_unique_component_identifier() == component_identifier:
                return component
            if isinstance(component, Group):
                result = component.get_component_by_identifier(component_identifier)
                if result is not None:
                    return result
        return None


    def identification(self):
        return "Group"

    def draw(self, canvas):
        for component in self.components:
            component.draw(canvas)

    def print(self, child_number):
        """
        print single image

        Args:
            child_number (int): Index of single image inside root children
        """
        print("|")
        print("-- ", self.identification(), " ", child_number)
        print("  |")
        print("   --Components: ")
        for (compNumber, comp) in enumerate(self.components):
            comp.print(compNumber)


    def print_latex(self):
        """
        print single image in latex syntax
        """

        output = ""
        output += self.identification()
        output += "["
        for (_, comp) in enumerate(self.components):
            output += "["
            output += comp.print_latex()
            output += "]"
        output += "]"
        return output