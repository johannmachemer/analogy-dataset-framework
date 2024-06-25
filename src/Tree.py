from Attribute import (Size, Type)
import subprocess
import os

class TreeNode(object):

    def __init__(self):
        pass

    def print(self):
        pass



class Root(TreeNode):

    def __init__(self, rule_set):
        self.children_analogie = []
        self.children_answer = []
        self.rule_set = rule_set

    def insertAnalogie(self, node):
        self.children_analogie.append(node)

    def insertAnswer(self, node):
        self.children_answer.append(node)

    def print(self):
        print("Root")
        for (childNumber,child) in enumerate(self.children_analogie):
            child.print(childNumber)
        for (childNumber,child) in enumerate(self.children_answer):
            child.print(childNumber)

    def saveLatex(self, file_name):
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

        os.chdir("latex")

        with open("tree.tex", "w") as f:
            f.write(latex_code)
    
        # Kompiliere die .tex-Datei in eine PDF-Datei
        subprocess.run(["pdflatex", "tree.tex"])
        
        # Benenne die generierte PDF-Datei um
        subprocess.run(["mv", "tree.pdf", f"{file_name}.pdf"])


    def printLatex(self):
        ausgabe = "[Root "
        for (childNumber,child) in enumerate(self.children_analogie):
            ausgabe += "[ " 
            ausgabe += child.printLatex()
            ausgabe+= "]"

        ausgabe += "]"
        print(ausgabe)
        return ausgabe

    def sample(self):
        for child in self.children_analogie:
            child.sample()
        for child in self.children_answer:
            child.sample(ausgabe)


    def getRules(self):
        return self.rule_set


class SingleImage(TreeNode):

    def __init__(self):
        self.components = []

    def insertComponent(self, node):
        self.components.append(node)

    def sample(self):
        for component in self.components:
            component.sample()

    def print(self, childNumber):
        print("|")
        print("--Analogi Image ", childNumber)
        print("  |")
        print("   --Components: ")
        for (compnumber,comp) in enumerate(self.components):
            comp.print(compnumber)

    def printLatex(self):
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

    def __init__(self):
        self.type = Type()
        self.size = Size()

    def sample(self):
        self.size.sample()
        self.type.sample()
        

    def print(self, compNumber):
        print("     |")
        print("     --Component ", compNumber)
        print("       |")
        print("        --Type: ", self.type.get_value())
        print("        --Size: ", self.size.get_value())

    def printLatex(self):
        ausgabe = ""
        ausgabe += "Component"
        ausgabe += "[ Type: "
        ausgabe += f"{self.type.get_value()}"
        ausgabe += "]"
        ausgabe += "[ Size: "
        ausgabe += f"{self.size.get_value()}"
        ausgabe += "]"

        return ausgabe

    





    

    