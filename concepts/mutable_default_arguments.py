# EXAMPLE 1: Mutable default argument (list)
def add_employee(emp, emp_list=[]):
    # `emp_list` refers to the SAME list object on every call
    emp_list.append(emp)
    print(emp_list)


emps = ["John", "Jane"]

# passing an explicit list works as expected
add_employee("Aditya", emps)
# ['John', 'Jane', 'Aditya']

print()

# when no argument is passed, python uses the stored default list
# this list was created ONCE when the function was defined
print("current defaults:", add_employee.__defaults__)  # ([],)

add_employee("Corey")  # ['Corey']
print("current defaults:", add_employee.__defaults__)  # (['Corey'],)

add_employee("Casey")  # ['Corey', 'Casey']
print("current defaults:", add_employee.__defaults__)  # (['Corey', 'Casey'],)

add_employee("Jack")  # ['Corey', 'Casey', 'Jack']
print("current defaults:", add_employee.__defaults__)  # (['Corey', 'Casey', 'Jack'],)


print()


# FIX: Use `None` as a sentinel value
def add_employee_fixed(emp, emp_list=None):
    # a NEW list is created per function call when emp_list is None
    if emp_list is None:
        emp_list = []

    emp_list.append(emp)
    print(emp_list)


# the default never changes because None is immutable
print(add_employee_fixed.__defaults__)  # (None,)

add_employee_fixed("Aditya")
add_employee_fixed("Corey")

print(add_employee_fixed.__defaults__)  # (None,)


print()


# EXAMPLE 2: default arguments are evaluated at definition time

from datetime import datetime
import time


def display_time(time_to_print=datetime.now()):
    # datetime.now() was called ONCE when the function was defined
    print(time_to_print.strftime("%B %d, %Y %H:%M:%S"))


# all calls print the SAME timestamp
display_time()
time.sleep(1)
display_time()
time.sleep(1)
display_time()

print()


# FIX: use `None` as a sentinel value
def display_time_fixed(time_to_print=None):
    if time_to_print is None:
        time_to_print = datetime.now()

    print(time_to_print.strftime("%B %d, %Y %H:%M:%S"))


display_time_fixed()
time.sleep(1)
display_time_fixed()
time.sleep(1)
display_time_fixed()
