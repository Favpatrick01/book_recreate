from fastapi.testclient import TestClient
from main import app
from schemas.book import BookCreate, Books
from schemas.book import BookUpdate
from services.book import books
from uuid import UUID

client = TestClient(app)


def test_get_books():
    response = client.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_add_book():
    payload = {
        "title": "Johny bravo",
        "author": "John Doe",
        "year": 2023,
        "pages": 500,
        "language": "English"
    }
    response = client.post("/books", json=payload)
    data = response.json()
    assert data["message"] == "Book added successfully"
    assert data["data"]["title"] == "Johny bravo"


def test_get_book_by_id():
    payload = {
        "title": "Johny bravo",
        "author": "John Doe",
        "year": 2023,
        "pages": 500,
        "language": "English"
    }
    response = client.post("/books", json=payload)
    add_book_data = response.json()
    book_id = add_book_data['data']['id']
    get_response = client.get(f"/books/{book_id}")
    get_book_data = get_response.json()
    assert get_response.status_code == 200
    assert get_book_data['id'] == book_id


def test_get_book_by_id_not_found():
    book_id = 1
    get_response = client.get(f"/books/{book_id}")
    get_book_data = get_response.json()
    assert get_response.status_code == 404
    assert get_book_data['detail'] == "book not found."


def test_update_book():
   
    payload = {
        "title": "Johny bravo",
        "author": "John Doe",
        "year": 2023,
        "pages": 500,
        "language": "English"
    
    }
    get_response = client.post("/books/", json=payload)
    get_book_data = get_response.json()
    book_id = get_book_data['data']['id']

  
    update_payload = {
        "title": "Johnny Bravo Updated",
        "pages": 550
       
    }
    update_response = client.put(f"/books/{book_id}", json=update_payload)
    updated_data = update_response.json()
      
   
    assert update_response.status_code == 200
    assert updated_data["message"] == "Book updated successfully"
    assert updated_data["data"]["title"] == "Johnny Bravo Updated"
    assert updated_data["data"]["pages"] == 550



def test_update_book_not_found():
    fake_id = str(UUID(int=len(books) + 1))  
    update_payload = {
        "title": "Non-existent",
        "pages": 100
       
    }
    
    response = client.put(f"/books/{fake_id}", json=update_payload)
    data = response.json()

    assert response.status_code == 404
    assert "not found" in data["detail"]



def test_delete_book():
   
    payload = {
        "title": "Delete Me",
        "author": "John Doe",
        "year": 2024,
        "pages": 250,
        "language": "English"
    }
    create_response = client.post("/books", json=payload)
    created_book = create_response.json()
    book_id = created_book["data"]["id"]

   
    delete_response = client.delete(f"/books/{book_id}")
    delete_data = delete_response.json()

   
    assert delete_response.status_code == 200
    assert delete_data["message"] == "Book deleted successfully"

    
    get_response = client.get(f"/books/{book_id}")
    assert get_response.status_code == 404



def test_delete_book_not_found():
    fake_id = str(UUID(int=len(books) + 1)) 
    response = client.delete(f"/books/{fake_id}")
    data = response.json()

    assert response.status_code == 404
    assert "not found" in data["detail"]
