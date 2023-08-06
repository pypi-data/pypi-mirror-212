from mimetypes import init

class Person:
    def __init__(self, weight:float = 0.0, height: float = 0.0) -> None:
        self.weight = weight
        self.height = height
        pass

    def calculateBMI(self) -> float:
        '''
        Calculates person`s BMI
        '''

        return self.weight / (self.height * self.height)
    
    def getPersonBMIRange(self) -> str:

        person_BMI = self.calculateBMI()

        if person_BMI < 18.5:
            return "Baixo peso"
        elif person_BMI >= 18.5 and person_BMI < 25:
            return "Normal"
        elif person_BMI >= 25 and person_BMI < 30:
            return "Sobrepeso"
        elif person_BMI >= 30 and person_BMI < 35:
            return "Obesidade"
        elif person_BMI >= 35 and  person_BMI < 40:
            return "Obesidade grave"
        else:
            return "Obesidade muito grave"

