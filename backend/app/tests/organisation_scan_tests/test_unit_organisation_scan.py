import pytest 
from app.scanning.service import (
    split_file_name,
    to_camel_case,
    to_snake_case,
    to_pascal_case,
    to_kebab_case,
    is_camel_case,
    is_snake_case,
    is_pascal_case,
    is_kebab_case,
)

# Unit tests for the "to..." functions
# Checks that the functions correctly convert file names to the specified format

# camelCase tests
@pytest.mark.parametrize("file_name, expected", [
    ("employee_salary_report", "employeeSalaryReport"),
    ("employee-salary-report", "employeeSalaryReport"),
    ("employeeSalaryReport", "employeeSalaryReport"),
    ("EmployeeSalaryReport", "employeeSalaryReport"),
    ("employee", "employee"),
])
def test_to_camel_case(file_name, expected):
    assert to_camel_case(file_name) == expected

# snake_case tests
@pytest.mark.parametrize("file_name, expected", [
    ("employeeSalaryReport", "employee_salary_report"),
    ("employee-salary-report", "employee_salary_report"),
    ("EmployeeSalaryReport", "employee_salary_report"),
    ("employee salary report", "employee_salary_report"),
    ("employee", "employee"),
])
def test_to_snake_case(file_name, expected):
    assert to_snake_case(file_name) == expected

# PascalCase tests
@pytest.mark.parametrize("file_name,expected", [
    ("employee_salary_report", "EmployeeSalaryReport"),
    ("employee-salary-report", "EmployeeSalaryReport"),
    ("employeeSalaryReport", "EmployeeSalaryReport"),
    ("employee salary report", "EmployeeSalaryReport"),
    ("employee", "Employee"),
])
def test_to_pascal_case(file_name, expected):
    assert to_pascal_case(file_name) == expected

# kebab-case tests
@pytest.mark.parametrize("file_name, expected", [
    ("employeeSalaryReport", "employee-salary-report"),
    ("employee_salary_report", "employee-salary-report"),
    ("EmployeeSalaryReport", "employee-salary-report"),
    ("employee salary report", "employee-salary-report"),
    ("employee", "employee"),
])
def test_to_kebab_case(file_name, expected):
    assert to_kebab_case(file_name) == expected

# Edge case unit tests for the "to..." functions
def test_converters_handle_numbers():
    assert to_camel_case("Clientconfidential2026") == "clientConfidential2026"
    assert to_snake_case("Clientconfidential2026") == "client_confidential_2026"
    assert to_pascal_case("Clientconfidential2026") == "ClientConfidential2026"
    assert to_kebab_case("Clientconfidential2026") == "client-confidential-2026"

# Unit tests for the "is..." functions
# Checks that the functions correctly identify whether a file name is in the specified format
def test_is_camel_case():
    assert is_camel_case("employeeSalaryReport")
    assert not is_camel_case("employee_salary_report")

def test_is_snake_case():
    assert is_snake_case("employee_salary_report")
    assert not is_snake_case("employeeSalaryReport")

def test_is_pascal_case():
    assert is_pascal_case("EmployeeSalaryReport")
    assert not is_pascal_case("employeeSalaryReport")

def test_is_kebab_case():
    assert is_kebab_case("employee-salary-report")
    assert not is_kebab_case("employeeSalaryReport")

# Unit test for the split_file_name function
# Checks that the function correctly splits strings into English words (Word Ninja library)
@pytest.mark.parametrize("file_name, expected", [
    ("employee_salary_report", ["employee", "salary", "report"]),
    ("clientconfidentialagreement", ["client", "confidential", "agreement"]),
    ("financeandcredentialsoverview", ["finance", "and", "credentials", "overview"]),
    ("cyberinnovationhub", ["cyber", "innovation", "hub"]),
])
def test_split_file_name(file_name, expected):
    assert split_file_name(file_name) == expected

# Edge case unit tests for the split_file_name function

# Checks that Word Ninja ignores common separators when splitting file names into words
@pytest.mark.parametrize("file_name, expected", [
    ("dash-separated-file-name", ["dash", "separated", "file", "name"]),
    ("underscore_separated_file_name", ["underscore", "separated", "file", "name"]),
    ("file name with spaces", ["file", "name", "with", "spaces"]),
])
def test_split_file_name_ignores_separators(file_name, expected):
    assert split_file_name(file_name) == expected

# Checks that Word Ninja correctly splits file names with numbers into words and numbers
@pytest.mark.parametrize("file_name, expected", [
    ("clientconfidential2026", ["client", "confidential", "2026"]),
    ("employee_salary_report_2021", ["employee", "salary", "report", "2021"]),
])
def test_split_file_name_numbers(file_name, expected):
    assert split_file_name(file_name) == expected

