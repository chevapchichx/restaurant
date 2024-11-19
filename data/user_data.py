class User:
    def __init__(self, post, last_name, first_name, middle_name, birth_date, address, phone_number, salary):
        self.post = str(post)
        self.last_name = str(last_name)
        self.first_name = str(first_name)
        self.middle_name = str(middle_name)
        self.birth_date = str(birth_date)
        self.address = str(address)
        self.phone_number = str(phone_number)
        self.salary = int(salary)

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"

