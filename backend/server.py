from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timedelta
import jwt
import bcrypt
from bson import ObjectId


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# JWT Configuration
JWT_SECRET = os.environ.get('JWT_SECRET', 'christopher-merrick-secret-key-2024')
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24

# Create the main app
app = FastAPI(title="Christopher Merrick Database Consulting API")

# Security
security = HTTPBearer()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Helper function to convert ObjectId to string
def serialize_doc(doc):
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc

# ============================================================================
# MODELS
# ============================================================================

class BlogPost(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    title: str
    slug: str
    excerpt: str
    content: str
    category: str
    readTime: str = "5 min read"
    published: bool = True
    publishDate: datetime = Field(default_factory=datetime.utcnow)
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)
    seoTitle: Optional[str] = None
    seoDescription: Optional[str] = None

class BlogPostCreate(BaseModel):
    title: str
    slug: str
    excerpt: str
    content: str
    category: str
    readTime: str = "5 min read"
    published: bool = True
    seoTitle: Optional[str] = None
    seoDescription: Optional[str] = None

class Testimonial(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    name: str
    company: str
    location: str
    text: str
    rating: int = Field(ge=1, le=5)
    published: bool = True
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

class TestimonialCreate(BaseModel):
    name: str
    company: str
    location: str
    text: str
    rating: int = Field(ge=1, le=5)
    published: bool = True

class ContactSubmission(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    name: str
    email: EmailStr
    phone: Optional[str] = None
    company: Optional[str] = None
    consultationType: Optional[str] = None
    message: str
    status: str = "new"  # new, contacted, completed
    submittedAt: datetime = Field(default_factory=datetime.utcnow)
    notes: Optional[str] = None

class ContactSubmissionCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    company: Optional[str] = None
    consultationType: Optional[str] = None
    message: str

class Service(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    title: str
    description: str
    icon: str
    features: List[str]
    pricing: Optional[Dict[str, str]] = None
    published: bool = True
    order: int = 0
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

class ServiceUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    features: Optional[List[str]] = None
    pricing: Optional[Dict[str, str]] = None
    published: Optional[bool] = None
    order: Optional[int] = None

class AdminUser(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    email: EmailStr
    passwordHash: str
    name: str
    role: str = "admin"
    lastLogin: Optional[datetime] = None
    createdAt: datetime = Field(default_factory=datetime.utcnow)

class AdminLogin(BaseModel):
    email: EmailStr
    password: str

class NewsletterSubscription(BaseModel):
    email: EmailStr
    subscribedAt: datetime = Field(default_factory=datetime.utcnow)

# ============================================================================
# AUTHENTICATION
# ============================================================================

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None

async def get_current_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    admin = await db.admin_users.find_one({"email": payload.get("sub")})
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin user not found"
        )
    
    return serialize_doc(admin)

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

# ============================================================================
# PUBLIC ROUTES
# ============================================================================

@api_router.get("/")
async def root():
    return {"message": "Christopher Merrick Database Consulting API"}

@api_router.get("/blog", response_model=List[BlogPost])
async def get_blog_posts(skip: int = 0, limit: int = 10):
    """Get published blog posts with pagination"""
    posts = await db.blog_posts.find(
        {"published": True}
    ).sort("publishDate", -1).skip(skip).limit(limit).to_list(limit)
    
    return [serialize_doc(post) for post in posts]

@api_router.get("/blog/{slug}", response_model=BlogPost)
async def get_blog_post(slug: str):
    """Get single blog post by slug"""
    post = await db.blog_posts.find_one({"slug": slug, "published": True})
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return serialize_doc(post)

@api_router.get("/testimonials", response_model=List[Testimonial])
async def get_testimonials():
    """Get published testimonials"""
    testimonials = await db.testimonials.find(
        {"published": True}
    ).sort("createdAt", -1).to_list(100)
    
    return [serialize_doc(testimonial) for testimonial in testimonials]

@api_router.get("/services", response_model=List[Service])
async def get_services():
    """Get published services"""
    services = await db.services.find(
        {"published": True}
    ).sort("order", 1).to_list(100)
    
    return [serialize_doc(service) for service in services]

@api_router.post("/contact")
async def submit_contact_form(contact: ContactSubmissionCreate):
    """Submit contact form"""
    contact_dict = contact.dict()
    contact_dict["submittedAt"] = datetime.utcnow()
    contact_dict["status"] = "new"
    
    result = await db.contact_submissions.insert_one(contact_dict)
    
    return {
        "success": True,
        "message": "Thank you for your message. We'll get back to you within 24 hours.",
        "id": str(result.inserted_id)
    }

@api_router.post("/newsletter")
async def subscribe_newsletter(subscription: NewsletterSubscription):
    """Newsletter subscription"""
    # Check if email already exists
    existing = await db.newsletter_subscriptions.find_one({"email": subscription.email})
    if existing:
        return {"success": True, "message": "Email already subscribed"}
    
    await db.newsletter_subscriptions.insert_one(subscription.dict())
    return {"success": True, "message": "Successfully subscribed to newsletter"}

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
