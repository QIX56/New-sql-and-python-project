from flask import Flask, render_template, request, jsonify, redirect, url_for
from project import create_app
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from backend.models import User
from Schemas import UserRegister, UserLogin, ForgotPassword, ResetPassword, TokenResponse
from auth import hash_password, verify_password, create_access_token
from datetime import datetime, timedelta
import secrets

app = create_app()

@app.route('/', methods=['GET'])
def Index():
    return render_template('index.html')

@app.route('/about', methods=['GET'])
def about():
    return jsonify({'message': 'About!'})


@app.route('/contact', methods=['GET'])
def contact():
    return jsonify({'message': 'Contact!'})

if __name__ == '__main__':
    app.run(debug=True)

@app.route("/register", methods=['POST'])
def register(data: UserRegister, db: Session = Depends(get_db)):
    # Check if email already exists
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        name=data.name,
        email=data.email,
        password=data.password
    )
    db.add(user)
    db.commit()
    db.refresh(user)



""""
Syntax:

@app.get("/") Tells FastAPI that this function is the handler for GET requests to the root URL ("/").
def login(): Defines a function named read_root that will be called when a GET request is

////////////////////////////////////////////////////////////////////////////////////////////////

Arguments: UserLogin: This is a Pydantic model that defines the expected structure of the request body for the login endpoint. It includes fields for email and password.
db: Session = Depends(get_db): This argument uses FastAPI's dependency injection system to provide a database session to the function. 
The get_db function is called to create a new session, and FastAPI ensures that the session is properly closed after the request is processed.



"""
@app.route("/login", methods=['POST'])
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.email}
    )
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user_name=user.name,
        user_email=user.email
    )
