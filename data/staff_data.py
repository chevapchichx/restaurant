class Waiter_Data:
    def __init__(self, last_name, first_name, middle_name, address, phone_number, post, salary):
        self.last_name = str(last_name)
        self.first_name = str(first_name)
        self.middle_name = str(middle_name)
        self.address = str(address)
        self.phone_number = str(phone_number)
        self.post = str(post)
        self.salary = int(salary)

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"

