from Attribute import (Size, Type, Position, Filling)
import subprocess
import os

class TreeNode(object):
    """ Superclass of all tree nodes """

    def __init__(self):
        
        pass

    def print(self):
        pass



class Root(TreeNode):
    """ Root node"""

    def __init__(self, rule_set):
        """
        Instantiate a Root node.

        Args:
            rule_set (List(Rule)): a list of all rules on this analogy
        """

        # all children that are part of the analogy
        self.children_analogie = []
        # all children that are part of the possible answers
        self.children_answer = []
        self.rule_set = rule_set

    def insertAnalogie(self, node):
        """
        Insert a SingleImage to the analogy list

        Args:
            node (SingleImage): the SingleImage to insert
        """
        self.children_analogie.append(node)

    def insertAnswers(self, answerList):
        """
        Insert a List of SingleImages to the possible answer list

        Args:
            node (List(SingleImage)): the SingleImage to insert
        """
        self.children_answer.extend(answerList)

    def print(self):
        """
        print a root
        """
        print("Root")
        for (childNumber,child) in enumerate(self.children_analogie):
            child.print(childNumber)
        for (childNumber,child) in enumerate(self.children_answer):
            child.print(childNumber)

    def saveLatex(self, file_name):
        """
        Save root in latex syntax

        Args: 
            file_name (str): Name of file
        """
        ausgabe = self.printLatex()
        latex_code = f"""
            \\documentclass{{standalone}}
            \\usepackage{{forest}}

            \\begin{{document}}

            \\begin{{forest}}
            {ausgabe}
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


    def printLatex(self):
        """
        print root in latex syntax

        """
        ausgabe = "[Root "
        for (childNumber,child) in enumerate(self.children_analogie):
            ausgabe += "[ " 
            ausgabe += child.printLatex()
            ausgabe+= "]"
        for (childNumber,child) in enumerate(self.children_answer):
            ausgabe += "[ " 
            ausgabe += child.printLatex()
            ausgabe+= "]"

        ausgabe += "]"
        print(ausgabe)
        return ausgabe



    def sample(self):
        """
        sample root (recursive)

        """
        for child in self.children_analogie:
            child.sample()
        for child in self.children_answer:
            child.sample()


    def getRules(self):
        return self.rule_set


class SingleImage(TreeNode):
    """ Single Image node"""


    
    def __init__(self):
        """
        Instantiate a Single Image node.
        """
        # all children components
        self.components = []

    def insertComponent(self, node):
        """
        Insert a component to the Single Image node.

        """
        self.components.append(node)

    def sample(self):
        """
        sample single image (recursive)

        """
        for component in self.components:
            component.sample()



    def print(self, childNumber):
        """
        print single image

        Args:
            childNumber (int): Index of single image inside root children
        """
        print("|")
        print("--Analogi Image ", childNumber)
        print("  |")
        print("   --Components: ")
        for (compnumber,comp) in enumerate(self.components):
            comp.print(compnumber)

    def printLatex(self):
        """
        print single image in latex syntax
        """

        ausgabe = ""
        ausgabe += "Analogie Image"
        ausgabe += "["
        for (compnumber,comp) in enumerate(self.components):
            ausgabe += "["
            ausgabe += comp.printLatex()
            ausgabe += "]"
        ausgabe += "]"
        return ausgabe





class Component(TreeNode):
    """Component node"""
    

    def __init__(self):
        """
        Instantiate a component node.
        """

        # init Attributes
        self.type = Type()
        self.size = Size()
        self.position = Position()
        self.filling = Filling()

    def sample(self, attr = None):
        """
        sample a Single Image node. Sample either all attributes or one single attribute.

        Args:
            attr (String): The attribute that should be sampled (size, type, position or filling). If not set, ever attribute will be sampled
        """


        if attr == None:
            # sample every attribute
            self.size.sample()
            self.type.sample()
            self.position.sample((self.size.get_value(), self.size.get_value()))
            self.filling.sample()
            
        else:
            if attr == "size":
                self.size.sample()
                self.position.sample((self.size.get_value(), self.size.get_value()))
            elif attr == "type"  or attr == "corners":
                self.type.sample()
            elif attr == "position":
                self.position.sample()
            elif attr == "filling":
                self.filling.sample()

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

    def printLatex(self):
        """
        print component in latex syntax

        Args:
            compNumber (int): Index of component inside single image
        """
        ausgabe = ""
        ausgabe += "Component"
        ausgabe += "[ Type: "
        ausgabe += f"{self.type.get_value()}"
        ausgabe += "]"
        ausgabe += "[ Size: "
        ausgabe += f"{self.size.get_value()}"
        ausgabe += "]" 
        ausgabe += "[ Position: "
        ausgabe += f"\({self.position.get_value()[0]} \, {self.position.get_value()[1]}\)"
        ausgabe += "]"
        ausgabe += "[ Filling: "
        ausgabe += f"\({self.filling.get_value()}\)"
        ausgabe += "]"
        

        return ausgabe

    





    

    