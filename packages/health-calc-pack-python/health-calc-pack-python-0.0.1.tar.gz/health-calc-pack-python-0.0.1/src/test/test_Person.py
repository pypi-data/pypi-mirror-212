import re
from person.Person import Person

class TestBMICalculation:
    
    def test1(self):
        #Arrange
        person = Person()
        height = 1.80
        weight = 90

        #Act
        result = person.calculateBMI(weight, height)

        #Assert
        assert result == 27.777777777777775

        pass