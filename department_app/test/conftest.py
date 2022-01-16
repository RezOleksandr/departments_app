"""
Module containing unit tests base class
"""

# pylint: disable=C0103, no-member
import logging
import unittest
from datetime import date

from flask_testing import TestCase
from flask import current_app

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
        department1 = Department(department_name='TEST_DP1', department_phone_number='+380951515121')
        department2 = Department(department_name='TEST_DP2', department_phone_number='+380455411862')
        department3 = Department(department_name='TEST_DP3', department_phone_number='+380663123363')
        db.session.add(department1)
        db.session.add(department2)
        db.session.add(department3)
        db.session.commit()
        employee1 = Employee(employee_name='TEST_E1', position='Senior Developer', salary=500,
                             birthdate=date(1990, 1, 11), department_id=department1.department_id)
        employee2 = Employee(employee_name='TEST_E2', position='Middle Developer', salary=1000,
                             birthdate=date(1995, 2, 12), department_id=department1.department_id)
        employee3 = Employee(employee_name='TEST_E2', position='Junior Developer', salary=1500,
                             birthdate=date(2000, 3, 13), department_id=department2.department_id)
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
        db.create_all()
        self.populate_db()

    def tearDown(self):
        logger.debug("Running teardown")
        db.session.remove()
        db.drop_all()

    def test_app(self) -> None:
        """
        Test if testing app is created
        :return: None
        """
        logger.info("Testing app creation")
        assert self.app is not None
        assert current_app == self.app


if __name__ == '__main__':
    unittest.main()
