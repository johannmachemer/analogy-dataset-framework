from Attribute import (Size, Type, Position, Filling, Rotation)
import subprocess
import os

from src.Rule import Rule


class TreeNode(object):
    """ Superclass of all tree nodes """

    def __init__(self):
        
        pass

    def print(self):
        pass



class AnalogySample:
    """ Root node"""

    def __init__(self, analogy_rules:[Rule]):
        """
        Instantiate a Root node.

        Args:
            analogy_rules (List(Rule)): a list of all rules to create the analogy
        """
        super().__init__()

        # all children that are part of the analogy
        self.analogy = []
        # all children that are part of the possible answers
        self.candidates = []
        self.analogy_rules = analogy_rules

    def insert_analogy(self, node):
        """
        Insert a SingleImage to the analogy list

        Args:
            node (SingleImage): the SingleImage to insert
        """
        self.analogy.append(node)

    def insert_candidates(self, candidates):
        """
        Insert a List of SingleImages to the possible answer list

        Args:
            candidates (List(SingleImage)): the SingleImage to insert
        """
        self.candidates.extend(candidates)

    def print(self):
        """
        print a root
        """
        print("Root")
        for (childNumber,child) in enumerate(self.analogy):
            child.print(childNumber)
        for (childNumber,child) in enumerate(self.candidates):
            child.print(childNumber)

    def save_latex(self, file_name):
        """
        Save root in latex syntax

        Args: 
            file_name (str): Name of file
        """
        output = self.print_latex()
        latex_code = f"""
            \\documentclass{{standalone}}
            \\usepackage{{forest}}

            \\begin{{document}}

            \\begin{{forest}}
            {output}
            \\end{{forest}}

            \\end{{document}}
            """

        if not os.path.isdir("latex"):
            os.mkdir("latex")

        os.chdir("latex")

        with open("tree.tex", "w") as f:
            f.write(latex_code)
    
        # Kompiliere die .tex-Datei in eine PDF-Datei
        subprocess.run(["pdflatex", "tree.tex"])
        
        # Benenne die generierte PDF-Datei um
        subprocess.run(["mv", "tree.pdf", f"{file_name}.pdf"])

        os.chdir("..")


    def print_latex(self):
        """
        print root in latex syntax

        """
        output = "[Root "
        for (childNumber,child) in enumerate(self.analogy):
            output += "[ "
            output += child.print_latex()
            output+= "]"
        for (childNumber,child) in enumerate(self.candidates):
            output += "[ "
            output += child.print_latex()
            output+= "]"

        output += "]"
        print(output)
        return output

    def get_rules(self):
        return self.analogy_rules



class Component(TreeNode):
    """Component node"""
    

    def __init__(self):
        """
        Instantiate a component node.
        """
        super().__init__()

        # init Attributes
        self.type = Type()
        self.size = Size()
        self.rotation = Rotation()
        self.position = Position()
        self.filling = Filling()

    def sample(self, attr = None):
        """
        sample a Single Image node. Sample either all attributes or one single attribute.

        Args:
            attr (String): The attribute that should be sampled (size, type, position or filling). If not set, ever attribute will be sampled
        """


        if attr is None:
            # sample every attribute
            self.size.sample()
            self.type.sample()
            self.rotation.sample()
            self.position.sample(self.size.get_value())
            self.filling.sample()
            
        elif attr == "size":
            self.size.sample()
            self.position.sample(self.size.get_value())
        elif attr == "type" or attr == "corners":
            self.type.sample()
        elif attr == "position":
            self.position.sample()
        elif attr == "filling":
            self.filling.sample()
        elif attr == "rotation":
            self.rotation.sample()

    def print(self, compNumber):
        """
        print component

        Args:
            compNumber (int): Index of component inside single image
        """
        print("     |")
        print("     --Component ", compNumber)
        print("       |")
        print("        --Type: ", self.type.get_value())
        print("        --Size: ", self.size.get_value())
        print("        --Position: ", self.position.get_value())
        print("        --Filling: ", self.filling.get_value())
        print("        --Rotation: ", self.rotation.get_value())

    def print_latex(self):
        """
        print component in latex syntax
        """
        output = ""
        output += "Component"
        output += "[ Type: "
        output += f"{self.type.get_value()}"
        output += "]"
        output += "[ Size: "
        output += f"{self.size.get_value()}"
        output += "]"
        output += "[ Position: "
        output += f"\({self.position.get_value()[0]} \, {self.position.get_value()[1]}\)"
        output += "]"
        output += "[ Rotation: "
        output += f"\({self.rotation.get_value()}\)"
        output += "]"
        output += "[ Filling: "
        output += f"\({self.filling.get_value()}\)"
        output += "]"
        

        return output

class Group(Component):

    def __init__(self):
        """
        Instantiate a Single Image node.
        """
        super().__init__()
        # all children components
        self.components = []

    def insert_component(self, node):
        """
        Insert a component to the Single Image node.
        """
        self.components.append(node)

    def sample(self):
        """
        sample single image (recursive)
        """
        super().sample()
        self.sample_child_components()

    def sample_child_components(self):
        for component in self.components:
            component.sample()

    def print(self, childNumber):
        """
        print single image

        Args:
            childNumber (int): Index of single image inside root children
        """
        print("|")
        print("-- ",self.identification(), " ", childNumber)
        print("  |")
        print("   --Components: ")
        for (compNumber, comp) in enumerate(self.components):
            comp.print(compNumber)

    def identification(self):
        return "Group"

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
class SingleImage(Group):
    """ Single Image node"""

    def identification(self):
        return "Image"
