"""
Module containing unit tests base class
"""

# pylint: disable=C0103, no-member
import logging
import unittest
from datetime import date

from flask_testing import TestCase

from department_app import create_app
from department_app.database import db
from department_app.models import Department, Employee

logging.basicConfig(filename='test_log.log',
                    filemode='a',
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)


class BaseTest(TestCase):
    """
    Base test case class
    """
    @staticmethod
    def populate_db():
        """
        Method to populate database with test data
        """
        logger.debug("Populating database")
        department1 = Department(department_name='TEST_DP1', department_phone_number='+381111111111')
        department2 = Department(department_name='TEST_DP2', department_phone_number='+382222222222')
        department3 = Department(department_name='TEST_DP3', department_phone_number='+383333333333')
        db.session.add(department1)
        db.session.add(department2)
        db.session.add(department3)
        db.session.commit()
        employee1 = Employee(employee_name='TEST_E1', position='Test Subject 1', salary=111,
                             birthdate=date(1991, 1, 11), department_id=department1.department_id)
        employee2 = Employee(employee_name='TEST_E2', position='Test Subject 2', salary=222,
                             birthdate=date(1992, 2, 12), department_id=department1.department_id)
        employee3 = Employee(employee_name='TEST_E3', position='Test Subject 3', salary=333,
                             birthdate=date(1993, 3, 13), department_id=department2.department_id)
        db.session.add(employee1)
        db.session.add(employee2)
        db.session.add(employee3)
        db.session.commit()

    def create_app(self):
        logger.debug("Creating app")
        app = create_app(test_config=True)
        app.config['TESTING'] = True
        return app

    def setUp(self):
        logger.debug("Running setup")
        self.app = self.create_app().test_client()
        db.create_all()
        self.populate_db()

    def tearDown(self):
        logger.debug("Running teardown")
        db.session.remove()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()
