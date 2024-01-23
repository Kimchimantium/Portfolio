from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    parent_id = Column(Integer, ForeignKey('parent.id'))
    parent = relationship("Parent")

# Example usage:
parent = Parent(name="Parent 1")
child1 = Child(name="Child 1", parent=parent)
child2 = Child(name="Child 2", parent=parent)

# Accessing children from parent
print(parent.children)  # Outputs: [<Child(name='Child 1')>, <Child(name='Child 2')>]
