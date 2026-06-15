# Social Media Post API

A professional-grade REST API for social media posts management built with FastAPI, PostgreSQL, and JWT authentication.

## SDG Alignment

This project supports *SDG 9 – Industry, Innovation, and Infrastructure
This project aligns with United Nations Sustainable Development Goal 9: Industry, Innovation, and Infrastructure. By building an open-source, industry-standard API tailored for Sierra Leone.

## Features

- OAuth2 + JWT Authentication
- Role-based Access Control (Admin/User)
- CRUD Operations for Posts, Comments, Likes
- Async/Await for I/O-bound operations
- Dependency Injection
- Automatic Documentation (Swagger UI / ReDoc)
- PostgreSQL with SQLAlchemy ORM
- Type Annotations throughout

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Setup PostgreSQL database
createdb social_media_db

# 3. Run application
uvicorn main:app --reload