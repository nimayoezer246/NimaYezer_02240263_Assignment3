import unittest
from NimaYezer_02240263_A3_PA import Account, BankingSystem

class TestBankingApplication(unittest.TestCase):

    def setUp(self):
        self.bank = BankingSystem()
        self.acc1 = self.bank.create_account("Personal")
        self.acc2 = self.bank.create_account("Business")

    def test_deposit(self):
        result = self.acc1.deposit(100)
        self.assertEqual(self.acc1.funds, 100)
        self.assertIn("deposited", result)

    def test_withdraw_success(self):
        self.acc1.deposit(200)
        result = self.acc1.withdraw(100)
        self.assertEqual(self.acc1.funds, 100)
        self.assertIn("withdrawn", result)

    def test_withdraw_failure(self):
        result = self.acc1.withdraw(100)
        self.assertIn("Insufficient", result)

    def test_transfer_success(self):
        self.acc1.deposit(300)
        result = self.acc1.transfer(150, self.acc2)
        self.assertEqual(self.acc1.funds, 150)
        self.assertEqual(self.acc2.funds, 150)
        self.assertIn("transferred", result)

    def test_transfer_failure(self):
        result = self.acc1.transfer(100, self.acc2)
        self.assertIn("Insufficient", result)

    def test_top_up_success(self):
        self.acc1.deposit(100)
        result = self.acc1.top_up_phone(50)
        self.assertEqual(self.acc1.funds, 50)
        self.assertEqual(self.acc1.phone_balance, 50)
        self.assertIn("topped up", result)

    def test_top_up_failure(self):
        result = self.acc1.top_up_phone(50)
        self.assertIn("Insufficient", result)

    def test_login_success(self):
        login = self.bank.login(self.acc1.account_id, self.acc1.passcode)
        self.assertEqual(login, self.acc1)

    def test_login_failure(self):
        login = self.bank.login("wrongid", "wrongpass")
        self.assertIsNone(login)

if __name__ == '__main__':
    unittest.main()
