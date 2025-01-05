# FastAPI SQLAlchemy structure with nested models

A common problem when using FastAPI comes from handling circular references.

* E.g. you have a User model and a Post model, now you want to register User.posts and Post.user.
* Furthermore you wish to have routes that return a User with all the associated posts and similar a Post with the associated User.


Pydantic V2 does not seem to handle this peticular problem well if you want to define all models and schemas in just two separate files (e.g. "post.models.py" and "user.models.py"). In V1, you could use update_forward_ref to solve this, but this doesn't seem to work in Pydantic V2 (neither using update_forward_refs, nor using model_rebuild). A "solution" is to use a shared models folder and handle model_rebuilds in the "\__init\__.py" file. However, if you want to use a modular domain-driven structure you're out of luck.

## Solution

The solution proposed here is simply to:

1. Use SQLAlchemy instead of SQLModel, which handles typing and circular references well through TYPE_CHECKING imports.
2. Keep the SQLAlchemy model and CRUD Pydantic models (UserBase, UserCreate, UserRead, UserUpdate) in models.py for the domains (e.g. user.models.py).
3. Put models that require nesting in a separate file: schemas.py or nested.py (UserReadWithPosts) that imports from both user.models and post.models
4. Import models freely in services and routes as required without circular reference problems.