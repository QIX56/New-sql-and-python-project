from flask import Flask, render_template, request, jsonify, redirect, url_for
from project import create_app
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
# from database import get_db
from project.models import User
from Schemas import UserRegister, UserLogin, ForgotPassword, ResetPassword, TokenResponse
#from auth import hash_password, verify_password, create_access_token
from datetime import datetime, timedelta
from pydantic import ValidationError
from Schemas import UserRegister, UserLogin
from project.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from project import create_app, db

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



@app.route("/register", methods=['POST'])
def register():
    try:
        data = UserRegister.model_validate(request.get_json())
    except ValidationError as e:
        return jsonify(e.errors(include_context=False)), 400

    if db.session.scalar(db.select(User).filter_by(email=data.email)):
        return jsonify(error="That email is already registered"), 409


    #hashed = generate_password_hash(data.password)  # never store the plain password
    student_id = data.email.split("@")[0]           # the 10 digits before @student.csn.edu

    user = User(first_name=data.first_name, last_name=data.last_name, email=data.email, 
                password=data.password)
    db.session.add(user)
    db.session.commit()
    return jsonify(message="Account created"), 201

if __name__ == '__main__':
    app.run(debug=True)

""""
Syntax:

@app.get("/") Tells FastAPI that this function is the handler for GET requests to the root URL ("/").
def login(): Defines a function named read_root that will be called when a GET request is

////////////////////////////////////////////////////////////////////////////////////////////////

Arguments: UserLogin: This is a Pydantic model that defines the expected structure of the request body for the login endpoint. It includes fields for email and password.
db: Session = Depends(get_db): This argument uses FastAPI's dependency injection system to provide a database session to the function. 
The get_db function is called to create a new session, and FastAPI ensures that the session is properly closed after the request is processed.




@app.route("/login", methods=['POST'])
def login(data: UserLogin, db: Session = Depends(db.session)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    #access_token = create_access_token(data={"sub": user.email}
    )
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user_name=user.name,
        user_email=user.email
    )
"""

