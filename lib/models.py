from sqlalchemy import ForeignKey, Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Role(Base):
    __tablename__ = 'roles'
    
    id = Column(Integer(), primary_key=True)
    character_name = Column(String())

    # Relationship to auditions
    auditions = relationship('Audition', backref='role')

    def actors(self):
        '''Returns a list of actor names for the role's auditions.'''
        return [audition.actor for audition in self.auditions]

    def locations(self):
        '''Returns a list of locations for the role's auditions.'''
        return [audition.location for audition in self.auditions]

    def lead(self):
        '''Returns the first audition that was hired for the role.'''
        lead_audition = next((audition for audition in self.auditions if audition.hired), None)
        return lead_audition or 'no actor has been hired for this role'

    def understudy(self):
        '''Returns the second audition that was hired for the role.'''
        hired_auditions = [audition for audition in self.auditions if audition.hired]
        if len(hired_auditions) >= 2:
            return hired_auditions[1]
        return 'no actor has been hired for understudy for this role'


class Audition(Base):
    __tablename__ = 'auditions'

    id = Column(Integer(), primary_key=True)
    actor = Column(String())
    location = Column(String())
    phone = Column(Integer())
    hired = Column(Boolean, default=False)

    # Foreign key to Role
    role_id = Column(Integer(), ForeignKey('roles.id'))

    def call_back(self):
        '''Marks the audition as hired.'''
        self.hired = True
