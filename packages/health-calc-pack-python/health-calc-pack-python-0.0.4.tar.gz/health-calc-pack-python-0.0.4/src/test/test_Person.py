import re
from person.Person import Person

class TestPersonClass:
    
    def testBMICalculation(self):
        #Arrange
        person = Person(90, 1.80)

        #Act
        result = person.calculateBMI()

        #Assert
        assert result == 27.777777777777775

        pass
    
    def testBMIRange(self):
        #Arrange
        person = Person(90, 1.80)

        #Act
        result = person.getPersonBMIRange()

        #Assert
        assert result == "Sobrepeso"

        pass