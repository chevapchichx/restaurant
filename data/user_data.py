from enum import IntEnum

class User_Role(IntEnum):
    WAITER = 1
    COOK = 2
    ADMIN = 3

class User:
    __role = 0

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"
    
    @property
    def role_name(self):
        return self.__get_role_name()
    
    @property
    def role(self):
        return self.__role
    
    def __init__(self, role, job, last_name, first_name, middle_name, birth_date, address, phone_number, salary, login, password):
        self.__role = int(role)
        self.job = str(job)
        self.last_name = str(last_name)
        self.first_name = str(first_name)
        self.middle_name = str(middle_name)
        self.birth_date = str(birth_date)
        self.address = str(address)
        self.phone_number = str(phone_number)
        self.salary = int(salary)
        self.login = str(login)
        self.password = str(password)

    def __get_role_name(self):
        if self.role == User_Role.WAITER:
            return "Официант"
        elif self.role == User_Role.COOK:
            return "Повар"
        elif self.role == User_Role.ADMIN:
            return "Администратор"
        else:
            return "Неизвестно"