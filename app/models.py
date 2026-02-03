from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    password: str

    # Task 3.1: User has todos
    todos: list["Todo"] = Relationship(back_populates="user")

    def set_password(self, plaintext_password):
        self.password = password_hash.hash(plaintext_password)

    def __str__(self) -> str:
        return f"(User id={self.id}, username={self.username}, email={self.email})"


class TodoCategory(SQLModel, table=True):
    # Many-to-many join table between Todo and Category
    todo_id: int = Field(foreign_key="todo.id", primary_key=True)
    category_id: int = Field(foreign_key="category.id", primary_key=True)


class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    text: str = Field(max_length=255)

    # Relationship to todos via join table
    todos: list["Todo"] = Relationship(back_populates="categories", link_model=TodoCategory)


class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    text: str = Field(max_length=255)
    done: bool = Field(default=False)

    # Relationship to user
    user: User = Relationship(back_populates="todos")
    # Relationship to categories via join table
    categories: list["Category"] = Relationship(back_populates="todos", link_model=TodoCategory)

    def toggle(self):
        self.done = not self.done
