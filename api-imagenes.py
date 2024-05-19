from fastapi import FastAPI, HTTPException
import mysql.connector
from pydantic import BaseModel
from typing import List
import schemas

app = FastAPI()

host_name = "44.213.9.26"
port_number = 8005
user_name = "root"
password_db = "utec"
database_name = "apiimagenes"

# Get all images
@app.get("/images", response_model=List[schemas.Image])
def get_images():
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM images")
    result = cursor.fetchall()
    mydb.close()
    return result

# Get an image by ID
@app.get("/images/{id}", response_model=schemas.Image)
def get_image(id: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM images WHERE id = {id}")
    result = cursor.fetchone()
    mydb.close()
    if result is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return result

# Add a new image
@app.post("/images", response_model=schemas.Image)
def add_image(image: schemas.Image):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    sql = "INSERT INTO images (name, description, url) VALUES (%s, %s, %s)"
    val = (image.name, image.description, image.url)
    cursor.execute(sql, val)
    mydb.commit()
    image_id = cursor.lastrowid
    mydb.close()
    return { "id": image_id, **image.dict() }

# Modify an image
@app.put("/images/{id}", response_model=schemas.Image)
def update_image(id: int, image: schemas.Image):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    sql = "UPDATE images SET name=%s, description=%s, url=%s WHERE id=%s"
    val = (image.name, image.description, image.url, id)
    cursor.execute(sql, val)
    mydb.commit()
    mydb.close()
    return { "id": id, **image.dict() }

# Delete an image by ID
@app.delete("/images/{id}")
def delete_image(id: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"DELETE FROM images WHERE id = {id}")
    mydb.commit()
    mydb.close()
    return {"message": "Image deleted successfully"}
