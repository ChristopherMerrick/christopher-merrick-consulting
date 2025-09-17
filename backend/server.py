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
    
# ============================================================================
# ADMIN ROUTES
# ============================================================================

@api_router.post("/auth/login")
async def login(login_data: AdminLogin):
    """Admin login"""
    admin = await db.admin_users.find_one({"email": login_data.email})
    if not admin or not verify_password(login_data.password, admin["passwordHash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Update last login
    await db.admin_users.update_one(
        {"_id": admin["_id"]},
        {"$set": {"lastLogin": datetime.utcnow()}}
    )
    
    access_token = create_access_token(data={"sub": admin["email"]})
    return {"access_token": access_token, "token_type": "bearer"}

@api_router.get("/auth/me")
async def get_current_user(current_admin = Depends(get_current_admin)):
    """Get current admin user"""
    return {"email": current_admin["email"], "name": current_admin["name"], "role": current_admin["role"]}

# Blog Management
@api_router.get("/admin/blog", response_model=List[BlogPost])
async def get_all_blog_posts(current_admin = Depends(get_current_admin), skip: int = 0, limit: int = 50):
    """Get all blog posts including drafts"""
    posts = await db.blog_posts.find().sort("createdAt", -1).skip(skip).limit(limit).to_list(limit)
    return [serialize_doc(post) for post in posts]

@api_router.post("/admin/blog", response_model=BlogPost)
async def create_blog_post(post: BlogPostCreate, current_admin = Depends(get_current_admin)):
    """Create new blog post"""
    post_dict = post.dict()
    post_dict["createdAt"] = datetime.utcnow()
    post_dict["updatedAt"] = datetime.utcnow()
    post_dict["publishDate"] = datetime.utcnow()
    
    result = await db.blog_posts.insert_one(post_dict)
    created_post = await db.blog_posts.find_one({"_id": result.inserted_id})
    return serialize_doc(created_post)

@api_router.put("/admin/blog/{post_id}", response_model=BlogPost)
async def update_blog_post(post_id: str, post: BlogPostCreate, current_admin = Depends(get_current_admin)):
    """Update blog post"""
    post_dict = post.dict()
    post_dict["updatedAt"] = datetime.utcnow()
    
    result = await db.blog_posts.update_one(
        {"_id": ObjectId(post_id)},
        {"$set": post_dict}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Blog post not found")
    
    updated_post = await db.blog_posts.find_one({"_id": ObjectId(post_id)})
    return serialize_doc(updated_post)

@api_router.delete("/admin/blog/{post_id}")
async def delete_blog_post(post_id: str, current_admin = Depends(get_current_admin)):
    """Delete blog post"""
    result = await db.blog_posts.delete_one({"_id": ObjectId(post_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return {"success": True, "message": "Blog post deleted"}

# Testimonial Management
@api_router.get("/admin/testimonials", response_model=List[Testimonial])
async def get_all_testimonials(current_admin = Depends(get_current_admin)):
    """Get all testimonials"""
    testimonials = await db.testimonials.find().sort("createdAt", -1).to_list(100)
    return [serialize_doc(testimonial) for testimonial in testimonials]

@api_router.post("/admin/testimonials", response_model=Testimonial)
async def create_testimonial(testimonial: TestimonialCreate, current_admin = Depends(get_current_admin)):
    """Create testimonial"""
    testimonial_dict = testimonial.dict()
    testimonial_dict["createdAt"] = datetime.utcnow()
    testimonial_dict["updatedAt"] = datetime.utcnow()
    
    result = await db.testimonials.insert_one(testimonial_dict)
    created_testimonial = await db.testimonials.find_one({"_id": result.inserted_id})
    return serialize_doc(created_testimonial)

@api_router.put("/admin/testimonials/{testimonial_id}", response_model=Testimonial)
async def update_testimonial(testimonial_id: str, testimonial: TestimonialCreate, current_admin = Depends(get_current_admin)):
    """Update testimonial"""
    testimonial_dict = testimonial.dict()
    testimonial_dict["updatedAt"] = datetime.utcnow()
    
    result = await db.testimonials.update_one(
        {"_id": ObjectId(testimonial_id)},
        {"$set": testimonial_dict}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Testimonial not found")
    
    updated_testimonial = await db.testimonials.find_one({"_id": ObjectId(testimonial_id)})
    return serialize_doc(updated_testimonial)

@api_router.delete("/admin/testimonials/{testimonial_id}")
async def delete_testimonial(testimonial_id: str, current_admin = Depends(get_current_admin)):
    """Delete testimonial"""
    result = await db.testimonials.delete_one({"_id": ObjectId(testimonial_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Testimonial not found")
    return {"success": True, "message": "Testimonial deleted"}

# Contact Management
@api_router.get("/admin/contacts")
async def get_contact_submissions(current_admin = Depends(get_current_admin), skip: int = 0, limit: int = 50):
    """Get contact submissions"""
    contacts = await db.contact_submissions.find().sort("submittedAt", -1).skip(skip).limit(limit).to_list(limit)
    return [serialize_doc(contact) for contact in contacts]

@api_router.put("/admin/contacts/{contact_id}")
async def update_contact_status(contact_id: str, status: str, notes: Optional[str] = None, current_admin = Depends(get_current_admin)):
    """Update contact status and notes"""
    update_data = {"status": status}
    if notes:
        update_data["notes"] = notes
    
    result = await db.contact_submissions.update_one(
        {"_id": ObjectId(contact_id)},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Contact submission not found")
    
    return {"success": True, "message": "Contact updated"}

# Service Management
@api_router.get("/admin/services", response_model=List[Service])
async def get_all_services(current_admin = Depends(get_current_admin)):
    """Get all services"""
    services = await db.services.find().sort("order", 1).to_list(100)
    return [serialize_doc(service) for service in services]

@api_router.put("/admin/services/{service_id}", response_model=Service)
async def update_service(service_id: str, service: ServiceUpdate, current_admin = Depends(get_current_admin)):
    """Update service"""
    service_dict = {k: v for k, v in service.dict().items() if v is not None}
    service_dict["updatedAt"] = datetime.utcnow()
    
    result = await db.services.update_one(
        {"_id": ObjectId(service_id)},
        {"$set": service_dict}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Service not found")
    
    updated_service = await db.services.find_one({"_id": ObjectId(service_id)})
    return serialize_doc(updated_service)

# Analytics
@api_router.get("/admin/analytics")
async def get_analytics(current_admin = Depends(get_current_admin)):
    """Get basic analytics"""
    total_contacts = await db.contact_submissions.count_documents({})
    new_contacts = await db.contact_submissions.count_documents({"status": "new"})
    total_testimonials = await db.testimonials.count_documents({"published": True})
    total_blog_posts = await db.blog_posts.count_documents({"published": True})
    newsletter_subscribers = await db.newsletter_subscriptions.count_documents({})
    
    # Recent contacts
    recent_contacts = await db.contact_submissions.find().sort("submittedAt", -1).limit(5).to_list(5)
    
    return {
        "totalContacts": total_contacts,
        "newContacts": new_contacts,
        "totalTestimonials": total_testimonials,
        "totalBlogPosts": total_blog_posts,
        "newsletterSubscribers": newsletter_subscribers,
        "recentContacts": [serialize_doc(contact) for contact in recent_contacts]
    }

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
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

# Initialize default data
@app.on_event("startup")
async def initialize_data():
    """Initialize default admin user and sample data"""
    # Create default admin user if none exists
    existing_admin = await db.admin_users.find_one({"email": "admin@christophermerrick.co.uk"})
    if not existing_admin:
        default_admin = AdminUser(
            email="admin@christophermerrick.co.uk",
            passwordHash=hash_password("admin123"),
            name="Site Administrator"
        )
        await db.admin_users.insert_one(default_admin.dict())
        logger.info("Created default admin user: admin@christophermerrick.co.uk / admin123")
    
    # Initialize services if none exist
    services_count = await db.services.count_documents({})
    if services_count == 0:
        default_services = [
            {
                "title": "Custom Access Databases",
                "description": "Bespoke Microsoft Access databases designed to streamline your operations and unlock your organisation's potential.",
                "icon": "Database",
                "features": ["Custom forms and reports", "Data relationships", "User-friendly interfaces", "Scalable solutions"],
                "pricing": {
                    "basic": "£750 - £2,000",
                    "intermediate": "£2,000 - £7,500", 
                    "advanced": "£7,500+"
                },
                "published": True,
                "order": 1,
                "updatedAt": datetime.utcnow()
            },
            {
                "title": "Data Analysis & Insights",
                "description": "Transform raw data into actionable insights that drive informed business decisions and competitive advantage.",
                "icon": "BarChart3",
                "features": ["Data visualization", "Performance metrics", "Trend analysis", "Custom reporting"],
                "published": True,
                "order": 2,
                "updatedAt": datetime.utcnow()
            },
            {
                "title": "Database Consulting",
                "description": "Expert guidance on data strategy, optimization, and system integration. Available from 1-hour sessions to full-day reviews.",
                "icon": "Users",
                "features": ["System optimization", "Data strategy", "Process improvement", "Staff training"],
                "pricing": {
                    "hourly": "£80/hour",
                    "halfDay": "£300",
                    "fullDay": "£550"
                },
                "published": True,
                "order": 3,
                "updatedAt": datetime.utcnow()
            }
        ]
        
        await db.services.insert_many(default_services)
        logger.info("Initialized default services")
    
    # Initialize sample testimonials if none exist
    testimonials_count = await db.testimonials.count_documents({})
    if testimonials_count == 0:
        default_testimonials = [
            {
                "name": "Sarah Johnson",
                "company": "Johnson Manufacturing Ltd",
                "location": "Manchester",
                "text": "Christopher created an amazing system to track all our inventory and orders. It's saved us countless hours and improved our accuracy dramatically.",
                "rating": 5,
                "published": True,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            {
                "name": "David Wright",
                "company": "Wright Consulting",
                "location": "Birmingham",
                "text": "The database solution Christopher built has transformed how we manage client data. Professional service and excellent results.",
                "rating": 5,
                "published": True,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            {
                "name": "Emma Thompson",
                "company": "Thompson Logistics",
                "location": "Leeds",
                "text": "Highly recommend Christopher's services. He understood our complex requirements and delivered exactly what we needed.",
                "rating": 5,
                "published": True,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            }
        ]
        
        await db.testimonials.insert_many(default_testimonials)
        logger.info("Initialized sample testimonials")
    
    # Initialize sample blog posts if none exist
    blog_count = await db.blog_posts.count_documents({})
    if blog_count == 0:
        default_blog_posts = [
            {
                "title": "5 Signs Your Business Needs a Custom Database Solution",
                "slug": "5-signs-business-needs-custom-database-solution",
                "excerpt": "Discover when it's time to move beyond spreadsheets and invest in a proper database system.",
                "content": "# 5 Signs Your Business Needs a Custom Database Solution\n\nMany businesses start with spreadsheets, but as they grow, the limitations become apparent...",
                "category": "Database Strategy",
                "readTime": "5 min read",
                "published": True,
                "publishDate": datetime.utcnow(),
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow(),
                "seoTitle": "5 Signs Your Business Needs a Custom Database Solution | Christopher Merrick",
                "seoDescription": "Learn the key indicators that show when your business has outgrown spreadsheets and needs a professional database solution."
            },
            {
                "title": "Microsoft Access vs. Excel: Which is Right for Your Business?",
                "slug": "microsoft-access-vs-excel-comparison",
                "excerpt": "Understanding the key differences and when to make the switch from Excel to Access.",
                "content": "# Microsoft Access vs. Excel: Which is Right for Your Business?\n\nWhile both are Microsoft products, they serve very different purposes...",
                "category": "Technology Comparison",
                "readTime": "7 min read",
                "published": True,
                "publishDate": datetime.utcnow(),
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow(),
                "seoTitle": "Access vs Excel: Complete Comparison Guide | Christopher Merrick",
                "seoDescription": "Comprehensive comparison of Microsoft Access and Excel to help you choose the right tool for your business data management needs."
            }
        ]
        
        await db.blog_posts.insert_many(default_blog_posts)
        logger.info("Initialized sample blog posts")

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
