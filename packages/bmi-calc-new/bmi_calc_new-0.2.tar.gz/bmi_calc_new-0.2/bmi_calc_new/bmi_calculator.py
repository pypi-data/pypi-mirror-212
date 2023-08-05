class PersonForBMI:
    def __init__(self, age, weight, height,gender):
        self.age = age
        self.weight = weight
        self.height = height
        self.gender = gender
        self.bmi = 0

    def calculate_bmi(self):
        self.bmi = self.weight/(self.height/100)**2
        print(f"bmi=>{self.bmi}")

    def conclusion(self):
        if self.bmi <= 18.4:
            print("You are underweight.")
        elif self.bmi <= 24.9:
            print("Yo u are healthy.")
        elif self.bmi <= 29.9:
            print("You are over weight.")
        elif self.bmi <= 34.9:
            print("You are severely over weight.")
        elif self.bmi <= 39.9:
            print("You are obese.")
        else:
            print("You are severely obese.")