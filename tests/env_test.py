import json
import unittest

from prudentia.domain import Environment, Box


class TestEnvironment(unittest.TestCase):
    def setUp(self):
        self.env = Environment(id_env='env-test')
        self.test_box = Box('box-name', 'uname.yml', 'box-host', '0.0.0.0')
        self.env.add(self.test_box)

    def tearDown(self):
        self.env.remove(self.test_box)
        self.assertEqual(json.load(open(self.env_file_path(), 'r')), [])

    def env_file_path(self):
        return Environment.DEFAULT_ENVS_PATH + '/' + self.env.id_env + '/' + Environment.DEFAULT_ENV_FILE_NAME

    def test_env_file_is_valid(self):
        box = json.load(open(self.env_file_path(), 'r'))[0]
        self.assertEqual(box['name'], self.test_box.name)
        self.assertFalse('remote_user' in box)
        self.assertFalse('remote_pwd' in box)
        self.assertFalse('extra' in box)

    def test_add_existing_name(self):
        b2 = Box('box-name', 'dev2', 'box-hostname', '1.2.3.4')
        self.assertRaises(ValueError, self.env.add, b2)

    def test_get_valid_box(self):
        b = self.env.get('box-name')
        self.assertEqual(b.playbook, 'uname.yml')

    def test_get_not_valid_box(self):
        b = self.env.get('whatever')
        self.assertEqual(b, None)
