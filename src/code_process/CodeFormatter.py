from src.Block import Block
from src.code_process.CodeRemover import CodeRemover
from src.code_process.CodeReplacer import *


class CodeFormatter:
    """
    Cette class contient les méthodes qui permettent de modifier du code python pour qu'il intéragisse avec le terrain.
    """

    if FILE_LOGGING:
        logging.basicConfig(format=LOG_FORMAT, level=LOGGING_LEVEL)

    @staticmethod
    def format_code(code):
        """
        Remplace certaines instructions du code pris en parametre pour pouvoir lancer
        d'autres méthodes qui vont intéragir avec le jeu.
        :param code : Le code à formatter de l'utilisateur.
        :return : Le code formaté (avec les instructions remplacées.
        """
        assert (isinstance(code, str))

        code = CodeRemover.remove_unnecessary_blank_lines(code)

        code = code.replace('print("avance")', 'self.forward_animation()')
        code = code.replace("print('avance')", 'self.forward_animation()')
        code = code.replace('print("devant")', 'self.forward_animation()')
        code = code.replace("print('devant')", 'self.forward_animation()')
        code = code.replace('print("avancer")', 'self.forward_animation()')
        code = code.replace("print('avancer')", 'self.forward_animation()')

        code = code.replace('print("recule")', 'self.back_animation()')
        code = code.replace("print('recule')", 'self.back_animation()')
        code = code.replace('print("derriere")', 'self.back_animation()')
        code = code.replace("print('derriere')", 'self.back_animation()')
        code = code.replace('print("arriere")', 'self.back_animation()')
        code = code.replace("print('arriere')", 'self.back_animation()')

        code = code.replace('print("recule")', 'self.go_behind_animation()')
        code = code.replace("print('recule')", 'self.go_behind_animation()')
        code = code.replace('print("reculer")', 'self.go_behind_animation()')
        code = code.replace("print('reculer')", 'self.go_behind_animation()')

        code = code.replace('print("droite")', 'self.right_animation()')
        code = code.replace("print('droite')", 'self.right_animation()')

        code = code.replace('print("gauche")', 'self.left_animation()')
        code = code.replace("print('gauche')", 'self.left_animation()')

        code = CodeReplacer.add_self_to_functions(code)
        code = CodeReplacer.replace_assignments(code)
        code = CodeReplacer.replace_operations(code)

        logging.info(f"code has been formatted as follows :\n{code}")

        return code

    @staticmethod
    def append_variable_declarations(variable_dict, code):
        """
        Permet d'ajouter les instructions de déclaration de variable sur le terrain de jeu.
        :param variable_dict: le dictionnaire qui contient les noms et les valeurs des variables
        :param code: le code python à modifier
        :return : le code python avec les instructions de déclaration de variable
        """


        variables_str = ""
        for block in variable_dict.values():
            print(f"Nom de la variable : {block.variable_name}, Valeur de la variable : {block.variable_value}")
            if block is not None:
                if block.variable_value is None:
                    variables_str += block.variable_name + "=None\n"
                else:
                    variables_str += block.variable_name + "=" + str(block.variable_value) + "\n"

        print(variables_str + code)
        return variables_str + code
