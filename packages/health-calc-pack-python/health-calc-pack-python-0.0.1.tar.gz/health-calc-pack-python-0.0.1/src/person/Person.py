from mimetypes import init

class Person:
    def __init__(self) -> None:
        pass

    def calculateBMI(self, weight:float = 0.0, height: float = 0.0) -> float:
        '''
        Calculates person`s BMI
        '''

        return weight / (height * height)
        