"""Main application entry point for Social Media Post API."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import engine, Base
from app.routers import auth, users, posts, comments, likes

# Create all database tables on startup
Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    print("Social Media API starting up...")
    yield
    print("Social Media API shutting down...")


app = FastAPI(
    title="Social Media Post API",
    description="""
    A professional-grade REST API for social media posts management.
    
    ## Features
    - **User Authentication**: OAuth2 + JWT token-based authentication
    - **Posts Management**: Create, read, update, delete posts
    - **Comments**: Add comments to posts
    - **Likes**: Like/unlike posts
    - **Role-based Access**: Admin and regular user roles
    
    ## SDG Alignment
    This API supports **SDG 16: Peace, Justice, and Strong Institutions** by promoting
    digital governance, transparency, and community engagement through open-source
    collaborative platforms.
    
    ## Authentication
    Use the `/auth/login` endpoint to get your JWT token, then use it in the 
    Authorization header as: `Bearer <token>`
    """,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    contact={"name": "Social Media API Team", "email": "team@socialmediaapi.com"},
    license_info={"name": "MIT License", "url": "https://opensource.org/licenses/MIT"},
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(posts.router, prefix="/posts", tags=["Posts"])
app.include_router(comments.router, prefix="/comments", tags=["Comments"])
app.include_router(likes.router, prefix="/likes", tags=["Likes"])


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to Social Media Post API",
        "version": "1.0.0",
        "documentation": "/docs",
        "redoc": "/redoc",
        "sdg": "SDG 16: Peace, Justice, and Strong Institutions"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "social-media-api"}