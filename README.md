# easy-store

A simple object storing service built with FastAPI and backed with a SQLite database.
The API is a microservice that could be easily stood up and used with a front-end. SQLite will handle the creation of the database, the user just has to access the approriate endpoints.

This project stores JSON and File data, using 2 different endpoints `json` and `file`.
- The JSON data is stored within the SQLite database as a string.
- The File data is writen to memory and a reference to the path is stored along with other metadata.
