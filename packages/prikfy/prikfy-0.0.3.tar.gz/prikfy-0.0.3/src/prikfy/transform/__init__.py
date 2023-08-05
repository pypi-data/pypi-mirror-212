from ..utils.operation.number_to_word import number_to_word


class UnitTransform:
    def __init__(self):
        # Initialize any necessary variables or configurations
        pass

    def number_to_word(self, value):
        try:
            # Call the number_to_word function from prikfy.operation.number_to_word
            return number_to_word(value)
        except Exception as e:
            print("Warning: Error occurred while converting number to words. Returning original value.")
            return value
 


class Transformation:
    pass