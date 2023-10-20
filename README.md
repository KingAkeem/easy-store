# easy-store

This is a simple object storing service built with FastAPI and backed by an SQLite database. The API is designed to be a microservice that can be easily deployed and used in conjunction with a front-end application. This service enables you to store both JSON and file data, offering two distinct endpoints for each type of data.

## Features
- JSON Data Storage: The service can store JSON data within the SQLite database as a string.
- File Data Storage: It also allows you to write file data to memory and store a reference to the file path along with other metadata.

## Installation
Clone the repository:

```bash
git clone https://github.com/KingAkeem/easy-store.git
cd easy-store
```

### Using uvicorn 
```bash
pip install -r requirements.txt
```

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Using docker
```bash
docker build -t easy-store .
docker run -p 8000:8080 easy-store
```

The service will be available at http://localhost:8000.

## API Endpoints
### JSON Data Endpoint
- `POST /json`: Store JSON data in the SQLite database.
- `GET /json/{data_id}`: Retrieve stored JSON data by ID.
    - Query Params:
        - convert: bool = True | False - Converts the file to it's JSON representation instead of a string.

### File Data Endpoint
- `POST /file`: Upload and store file data.
- `GET /file/{file_id}`: Retrieve stored file data by ID.
    - Query Params:
        - convert: bool = True | False - Converts file to it's binary representation

## Usage
To use this service, you can make API requests using tools like curl, or you can create a front-end application to interact with the service. Below are some examples of API requests:

### Storing JSON Data
```bash
# POST JSON data
curl -X POST -H "Content-Type: application/json" -d '{"key": "value"}' http://localhost:8000/json

# GET JSON data as string by ID
curl http://localhost:8000/json/{data_id}

# GET JSON data by ID
curl http://localhost:8000/json/{data_id}?convert=True
```

### Storing File Data
```bash
# POST file data
curl -X POST -F "file=@/path/to/your/file" http://localhost:8000/file

# GET file data by ID
curl http://localhost:8000/file/{file_id}

# GET file binary data by ID
curl http://localhost:8000/file/{file_id}?convert=True
```

## Contributing
We welcome contributions! If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature: git checkout -b feature-name
3. Make your changes and commit them: git commit -m "Add your feature"
4. Push to the branch: git push origin feature-name
5. Submit a pull request.


## License
This project is licensed under the GPL-3.0 License - see the [LICENSE](https://github.com/KingAkeem/easy-store/blob/main/LICENSE) file for details.

## Contact
If you have any questions or need assistance, feel free to contact us at akeemtlking@gmail.com.