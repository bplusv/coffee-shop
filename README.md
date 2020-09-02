# FS Coffee Shop
FS Coffee Shop is menu application that allows users to view drink names and graphics representing the ratios of ingredients in each drink.

- Front-end built with Angular + Ionic framework.
- Back-end built with Python + Flask framework.
- Authentication & Roles with Auth0 service + JWT (JSON Web Tokens).
- Models and relationships with SQLAlchemy ORM, SQLite.

## Users Roles
- Public users can view the drinks names and graphics.
- Authenticated users with Barista role can view drink names, graphics, and ingredients details.
- Authenticated users with Manager roles can view drink names, graphics, indredientes details and create/edit/delete drinks.

## Backend

The `./backend` directory contains a Flask server.

[View the README.md within ./backend for more details.](./backend/README.md)

## Frontend

The `./frontend` directory contains a complete Ionic frontend to consume the data from the Flask server.

[View the README.md within ./frontend for more details.](./frontend/README.md)
