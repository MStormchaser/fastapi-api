import pytest
from app.calculations import add, BankAccount

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def default_bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("num1, num2, expected",[
                         (2,3,5),
                         (12,4,16),
                         (8,12,20)])
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected


def test_bank_set_initial_amout(default_bank_account):
    assert default_bank_account.balance == 50

def test_bank_default_amount(zero_bank_account):

    assert zero_bank_account.balance == 0

def test_withdraw(default_bank_account):
    default_bank_account.withdraw(20)
    assert default_bank_account.balance == 30

def test_deposit(default_bank_account):
    default_bank_account.deposit(30)
    assert default_bank_account.balance == 80

def test_collect_interest(default_bank_account):
    default_bank_account.collect_interest()
    assert round(default_bank_account.balance, 6) == 55

# if we want to tell pytest that we expect an exception we have to tell it so
def test_insufficient_funds(zero_bank_account):
    with pytest.raises(Exception):
        zero_bank_account.withdraw(200)
    
