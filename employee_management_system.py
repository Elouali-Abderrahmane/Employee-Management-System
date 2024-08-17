import csv

class Employee:

    COMPANY = "Elouali"
    PHONE_PREFIX = "+212"
    PHONE_LENGTH = 13

    def __init__(self, name: str, age: int, job: str, id: str, phone: str, bank_account:str, hours_worked: int=160, hourly_rate: int=15, from_file=False) -> None:
        self. name = name
        self. age = age
        self. job = job
        self. __id = id
        self. __phone = phone
        self. __bank_account = bank_account
        self. __hours_worked = hours_worked
        self. __hourly_rate = hourly_rate
        if not from_file:
            AllEmployee.add_employee(self)
    
    def __str__(self) -> str:
        return f"{self.name} is {self.age} years old and his work as {self.job}"
    
    def __repr__(self) -> str:
        return f"Employee(name: {self.name}, age: {self.age}, job: {self.job})"

    @property
    def id(self):
        return self.__id

    @property
    def hours_worked(self):
        return self.__hours_worked
    
    @property
    def hourly_rate(self):
        return self.__hourly_rate
    
    @hourly_rate.setter
    def hourly_rate(self, new_rate):
        if isinstance(new_rate, int) and new_rate > 0:
            self.__hourly_rate = new_rate
            print("The hourly rate is updated successfully!")
        else:
            print("The hourly rate should be a positive number")

    
    @property
    def phone(self):
        return self.__phone
    @staticmethod
    def is_valid_phone(phone):
        return phone.startswith("+212") and len(phone) == 13
    @phone.setter
    def phone(self, new_phone):
        if Employee.is_valid_phone(new_phone):
            self.__phone = new_phone
            print("Phone is updated successfully!")
        else:
            print("Invalid format phone")

    def get_bank_account(self, employee_id):
        if (employee_id == self.__id):
            return f"The bank account is {self.__bank_account}"
        else:
            return f"Invalid ID. You are not allowed to view the Bank Account"
        
    def calculate_gross_salary(self):
        return self.__hours_worked * self.__hourly_rate
    
    def calculate_net_salary(self):
        gross_salary = self.calculate_gross_salary()
        net_salary = Finance.calculate_net_salary(gross_salary)
        return net_salary



class AllEmployee:
    __employee = []

    @classmethod
    def add_employee(cls, employee):
        cls.__employee.append(employee)

    @classmethod
    def employees_list(cls):
        return cls.__employee
    
    @classmethod
    def get_employee_by_id(cls, employee_id):
        for employee in cls.__employee:
            if employee.id == employee_id:
                return employee
        return None
    
    @classmethod
    def remove_employee_by_id(cls, employee_id):
        for employee in cls.__employee:
            if employee.id == employee_id:
                # First way to remove the employee from the list                
                # cls.__employee.remove(employee) 

                # Second way to remove the employee from the list 
                cls.__employee = [employee for employee in cls.__employee if employee.id != employee_id]



class Finance:
    TAX_THRESHOLD = 5_000
    TAX_LOW = 0.04
    TAX_HIGHT = 0.07
    HEALTH_INSURANCE_COST = 100
    RETIREMENT_INSURANCE_RATE = 0.05

    @staticmethod
    def calculate_tax(gross_salary):
        if gross_salary < Finance.TAX_THRESHOLD:
            return gross_salary * Finance.TAX_LOW
        else:
            return gross_salary * Finance.TAX_HIGHT
    
    @staticmethod
    def calculate_net_salary(gross_salary):
        tax = Finance.calculate_tax(gross_salary)
        health_insurance = Finance.HEALTH_INSURANCE_COST
        retirement_insurance = Finance.RETIREMENT_INSURANCE_RATE * gross_salary
        net_salary = gross_salary - (tax + health_insurance + retirement_insurance)
        return net_salary




class EmployeeFileHandler:

    @staticmethod
    def read_csv_data(file_name):
        employees = []
        with open(file_name) as file:
            data_reader = csv.DictReader(file)
            for employee in data_reader:
                name = employee["name"]
                age = employee["age"]
                job = employee["job_title"]
                id = employee["id"]
                phone = employee["phone"]
                bank_account = employee["bank_account"]
                hours_worked = int(employee["hours_worked"])
                hourly_rate = int(employee["hour_rate"])
                employee = Employee(name, age, job, id, phone, bank_account, hours_worked, hourly_rate, from_file=True)
                employees.append(employee)
        return employees
    
    @staticmethod
    def read_and_add_to_AllEmployees(file_name):
        all_employees = EmployeeFileHandler.read_csv_data(file_name)
        for employee in all_employees:
            AllEmployee.add_employee(employee)



class Manager(Employee):
    BONUS = 500
    def __init__(self, authority_level, *args, **kwargs):
        self.__authority_level = authority_level
        super().__init__(* args, **kwargs)
    
    @property
    def auhtority_level(self):
        return self.__authority_level
    
    def promote_employee_by_id(self, employee_id, raise_amount):
        employee = AllEmployee.get_employee_by_id(employee_id)
        if employee:
            old_hourly_rate = employee.hourly_rate
            new_hourly_rate = old_hourly_rate + raise_amount
            employee.hourly_rate = new_hourly_rate
        else:
            print(f"The employee with {employee_id} ID is not found")
    
    def demote_employee_by_id(self, employee_id, decrease_amount):
        if self.__authority_level >= 2:
            employee = AllEmployee.get_employee_by_id(employee_id)
            if employee:
                old_hourly_rate = employee.hourly_rate
                new_hourly_rate = old_hourly_rate - decrease_amount
                employee.hourly_rate = max(new_hourly_rate, 5)
            else:
                print(f"The employee with {employee_id} ID is not found")
        else:
            print("You do not Have the authority to demote employees")
    
    def fired_employee_by_id(self, employee_id):
        if self.__authority_level >= 3:
            employee = AllEmployee.get_employee_by_id(employee_id)
            if employee:
                AllEmployee.remove_employee_by_id(employee_id)
                print(f"The employee with {employee_id} ID was fired")
            else:
                print(f"The employee with {employee_id} ID is not found")
        else:
            print("You do not Have the authority to fire employees")
    
    def __str__(self) -> str:
        based_message = super().__str__()
        return f"{based_message} and his authority level is {self.__authority_level}"
    
    def __repr__(self) -> str:
        return f'Manager (name: {self.name}, age: {self.age}, job: {self.job}, authority level: {self.__authority_level})'
    
    def calculate_gross_salary(self):
        base_gross_salary = super().calculate_gross_salary()
        new_gross_salary = base_gross_salary + Manager.BONUS
        return new_gross_salary



