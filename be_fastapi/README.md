# Simple FastAPI Application

A simple FastAPI application with basic CRUD operations for managing items.

## Features

- **GET** `/` - Welcome message
- **GET** `/health` - Health check endpoint
- **GET** `/items` - Get all items
- **GET** `/items/{item_id}` - Get item by ID
- **POST** `/items` - Create new item
- **PUT** `/items/{item_id}` - Update existing item
- **DELETE** `/items/{item_id}` - Delete item
- **GET** `/items/search/{name}` - Search items by name

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python main.py
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Access the API:**
   - API will be available at: `http://localhost:8000`
   - Interactive API docs (Swagger UI): `http://localhost:8000/docs`
   - Alternative API docs (ReDoc): `http://localhost:8000/redoc`

## API Usage Examples

### Create an item
```bash
curl -X POST "http://localhost:8000/items" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Laptop",
       "description": "Gaming laptop",
       "price": 999.99,
       "is_available": true
     }'
```

### Get all items
```bash
curl -X GET "http://localhost:8000/items"
```

### Get item by ID
```bash
curl -X GET "http://localhost:8000/items/1"
```

### Update an item
```bash
curl -X PUT "http://localhost:8000/items/1" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Updated Laptop",
       "description": "Updated gaming laptop",
       "price": 1099.99,
       "is_available": true
     }'
```

### Delete an item
```bash
curl -X DELETE "http://localhost:8000/items/1"
```

### Search items
```bash
curl -X GET "http://localhost:8000/items/search/laptop"
```

## Data Model

The application uses the following data model for items:

```json
{
  "id": 1,
  "name": "Item Name",
  "description": "Item description",
  "price": 99.99,
  "is_available": true
}
```

## Notes

- This is a simple in-memory storage implementation
- Data will be lost when the server restarts
- For production use, consider integrating with a proper database
