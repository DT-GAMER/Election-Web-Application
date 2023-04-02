import unittest
import register

class TestRegister(unittest.TestCase):

    def test_generate_key(self):
        key = register.generate_key()
        self.assertEqual(len(key), 24)

    def test_send_registration_email(self):
        email = 'abakpadominic0@gmail.com'
        key = 'A6hj23c27uh92u6678w92b34'
        try:
            register.send_registration_email(email, key)
        except Exception as e:
            self.fail(f"send_registration_email raised an exception: {e}")

    def test_register_user(self):
        full_name = 'Abakpa Dominic'
        email = 'abakpadominic0@gmail.com'
        try:
            register.register_user(full_name, email)
        except Exception as e:
            self.fail(f"register_user raised an exception: {e}")

if __name__ == '__main__':
    unittest.main()

