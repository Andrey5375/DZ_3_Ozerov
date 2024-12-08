import unittest
from io import StringIO
from config_parser import ConfigParser

class TestConfigParser(unittest.TestCase):
    def test_network_config(self):
        input_data = """
        =begin
        Конфигурация сети
        =cut
        network := {
            name : "LocalNetwork",
            ip_address : "192.168.1.1",
            subnet_mask : "255.255.255.0",
            gateway : "192.168.1.254",
            dns_servers : [ "8.8.8.8"; "8.8.4.4" ]
        }
        """
        expected_output = {
            "network": {
                "name": "LocalNetwork",
                "ip_address": "192.168.1.1",
                "subnet_mask": "255.255.255.0",
                "gateway": "192.168.1.254",
                "dns_servers": ["8.8.8.8", "8.8.4.4"]
            }
        }
        parser = ConfigParser()
        parser.parse(StringIO(input_data))
        self.assertEqual(parser.variables, expected_output)

    def test_database_config(self):
        input_data = """
        =begin
        Конфигурация базы данных
        =cut
        database := {
            host : "localhost",
            port : 5432,
            username : "admin",
            password : "secret",
            databases : [ "main_db"; "backup_db" ]
        }
        """
        expected_output = {
            "database": {
                "host": "localhost",
                "port": 5432,
                "username": "admin",
                "password": "secret",
                "databases": ["main_db", "backup_db"]
            }
        }
        parser = ConfigParser()
        parser.parse(StringIO(input_data))
        self.assertEqual(parser.variables, expected_output)

    def test_web_server_config(self):
        input_data = """
        =begin
        Конфигурация веб-сервера
        =cut
        web_server := {
            server_name : "example.com",
            document_root : "/var/www/html",
            listen_ports : [ 80; 443 ],
            ssl_certificate : "/etc/ssl/certs/example.com.crt",
            ssl_key : "/etc/ssl/private/example.com.key"
        }
        """
        expected_output = {
            "web_server": {
                "server_name": "example.com",
                "document_root": "/var/www/html",
                "listen_ports": [80, 443],
                "ssl_certificate": "/etc/ssl/certs/example.com.crt",
                "ssl_key": "/etc/ssl/private/example.com.key"
            }
        }
        parser = ConfigParser()
        parser.parse(StringIO(input_data))
        self.assertEqual(parser.variables, expected_output)

    def test_combined_config(self):
        input_data = """
        =begin
        Конфигурация сети
        =cut
        network := {
            name : "LocalNetwork",
            ip_address : "192.168.1.1",
            subnet_mask : "255.255.255.0",
            gateway : "192.168.1.254",
            dns_servers : [ "8.8.8.8"; "8.8.4.4" ]
        }

        =begin
        Конфигурация базы данных
        =cut
        database := {
            host : "localhost",
            port : 5432,
            username : "admin",
            password : "secret",
            databases : [ "main_db"; "backup_db" ]
        }

        =begin
        Конфигурация веб-сервера
        =cut
        web_server := {
            server_name : "example.com",
            document_root : "/var/www/html",
            listen_ports : [ 80; 443 ],
            ssl_certificate : "/etc/ssl/certs/example.com.crt",
            ssl_key : "/etc/ssl/private/example.com.key"
        }
        """
        expected_output = {
            "network": {
                "name": "LocalNetwork",
                "ip_address": "192.168.1.1",
                "subnet_mask": "255.255.255.0",
                "gateway": "192.168.1.254",
                "dns_servers": ["8.8.8.8", "8.8.4.4"]
            },
            "database": {
                "host": "localhost",
                "port": 5432,
                "username": "admin",
                "password": "secret",
                "databases": ["main_db", "backup_db"]
            },
            "web_server": {
                "server_name": "example.com",
                "document_root": "/var/www/html",
                "listen_ports": [80, 443],
                "ssl_certificate": "/etc/ssl/certs/example.com.crt",
                "ssl_key": "/etc/ssl/private/example.com.key"
            }
        }
        parser = ConfigParser()
        parser.parse(StringIO(input_data))
        self.assertEqual(parser.variables, expected_output)

if __name__ == '__main__':
    unittest.main()
