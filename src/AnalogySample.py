import subprocess
import os

import numpy as np
from src.Rule import Rule
from src.components.Group import Group
from src.const import SINGLE_IMAGE_WIDTH


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


class SingleImage(Group):
    """ Single Image node"""

    def __init__(self):
        super().__init__()

    def get_width(self):
        return SINGLE_IMAGE_WIDTH

    def get_absolut_position(self):
        return np.array([SINGLE_IMAGE_WIDTH / 2,SINGLE_IMAGE_WIDTH / 2])

    def get_filling(self):
        return 1

    def get_rotation(self):
        return 0

    def identification(self):
        return "Image"

    def sample(self, attr=None):
        super().sample_child_components(attr)
