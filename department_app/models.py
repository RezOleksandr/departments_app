import uuid

from sqlalchemy import Column, String, Float, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from department_app.database import db


class Department(db.Model):
    department_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    department_name = Column(String)
    department_phone_number = Column(String)

    employees = relationship("Employee", backref="department")

    def to_dict(self):
        return {
            'department_id': str(self.department_id),
            'department_name': self.department_name,
            'department_phone_number': self.department_phone_number,
            'employees': tuple(employee.to_dict() for employee in self.employees),
        }


class Employee(db.Model):
    employee_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employee_name = Column(String)
    position = Column(String)
    salary = Column(Float)
    birthdate = Column(Date)
    department_id = Column(UUID(as_uuid=True), ForeignKey('department.department_id'))

    def to_dict(self):
        return {
            'employee_id': str(self.employee_id),
            'employee_name': self.employee_name,
            'position': self.position,
            'salary': self.salary,
            'birthdate': str(self.birthdate),
            'department_id': str(self.department_id),
        }
