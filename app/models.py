from sqlalchemy import Integer, String, Text, JSON, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from typing import List, Dict

class Base(DeclarativeBase):
    pass

class Category(Base):
    __tablename__ = 'categories'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)

    subcategories: Mapped[list['Subcategory']] = relationship('Subcategory', back_populates='category')

    def __str__(self) -> str:
        return self.name

class Subcategory(Base):
    __tablename__ = 'subcategories'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)

    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('categories.id'))
    category: Mapped['Category'] = relationship('Category', back_populates='subcategories')

    problems: Mapped[list['Problem']] = relationship('Problem', back_populates='subcategory')

    def __str__(self) -> str:
        return self.name

class Problem(Base):
    __tablename__ = 'problems'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    constraints: Mapped[List[str]] = mapped_column(JSON, nullable=False)
    examples: Mapped[List[Dict[str, str]]] = mapped_column(JSON, nullable=False)
    image_paths: Mapped[List[str]] = mapped_column(JSON, nullable=False)    

    subcategory_id: Mapped[int] = mapped_column(Integer, ForeignKey('subcategories.id'), nullable=False)
    subcategory: Mapped['Subcategory'] = relationship('Subcategory', back_populates='problems')

    __table_args__ = (
        CheckConstraint('difficulty IN (1, 2, 3)', name='check_difficulty'),
    )

    def __str__(self) -> str:
        return self.title
