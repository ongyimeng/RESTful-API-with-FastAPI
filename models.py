from database import Base
from sqlalchemy import Column, String, Integer, UniqueConstraint, CheckConstraint


class User(Base):
    __tablename__ = "UsersTable"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    company = Column(String, nullable=True)
    designation = Column(String, nullable=True)

    __table_args__ = (
        UniqueConstraint("email"),
        CheckConstraint(
            role.in_(["ADMIN", "MEMBER", "TECHNICIAN"])
        )
    )
