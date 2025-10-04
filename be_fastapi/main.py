from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
import uvicorn
import os

# Get configuration from environment variables (ConfigMap)
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")
API_VERSION = os.getenv("API_VERSION", "v1")
DEBUG = os.getenv("DEBUG", "true").lower() == "true"

# Create FastAPI instance
app = FastAPI(
    title="Simple FastAPI App",
    description="A simple FastAPI application with basic CRUD operations",
    version="1.0.0",
    debug=DEBUG
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,  # From ConfigMap
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# In-memory storage (in a real app, you'd use a database)
items_db = []
next_id = 1

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to Simple FastAPI App!", "status": "running"}

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}

# Configuration endpoint
@app.get("/config")
async def get_config():
    return {
        "environment": ENVIRONMENT,
        "log_level": LOG_LEVEL,
        "cors_origins": CORS_ORIGINS,
        "api_version": API_VERSION,
        "debug": DEBUG
    }

# Get all items
@app.get("/items")
async def get_items():
    """Get all items from the database"""
    return items_db

# Get item by ID
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    """Get a specific item by ID"""
    for item in items_db:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

# Create new item
@app.post("/items")
async def create_item(item: Dict[str, Any]):
    """Create a new item"""
    global next_id
    new_item = {
        "id": next_id,
        "name": item.get("name", ""),
        "description": item.get("description", ""),
        "price": item.get("price", 0.0),
        "is_available": item.get("is_available", True)
    }
    items_db.append(new_item)
    next_id += 1
    return new_item

# Update item
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Dict[str, Any]):
    """Update an existing item"""
    for i, existing_item in enumerate(items_db):
        if existing_item["id"] == item_id:
            updated_item = {
                "id": item_id,
                "name": item.get("name", existing_item["name"]),
                "description": item.get("description", existing_item["description"]),
                "price": item.get("price", existing_item["price"]),
                "is_available": item.get("is_available", existing_item["is_available"])
            }
            items_db[i] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

# Delete item
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    """Delete an item by ID"""
    for i, item in enumerate(items_db):
        if item["id"] == item_id:
            deleted_item = items_db.pop(i)
            return {"message": f"Item '{deleted_item['name']}' deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")

# Search items by name
@app.get("/items/search/{name}")
async def search_items(name: str):
    """Search items by name (case-insensitive)"""
    matching_items = [
        item for item in items_db 
        if name.lower() in item["name"].lower()
    ]
    return matching_items

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
