# API Contracts & Integration Plan
## Christopher Merrick Database Consulting Website

### Overview
This document outlines the API contracts, data models, and integration strategy for converting the mock-based frontend to a fully functional CMS-enabled website.

## Database Models

### 1. Blog Posts (`blog_posts`)
```json
{
  "_id": "ObjectId",
  "title": "string",
  "slug": "string", // URL-friendly version
  "excerpt": "string",
  "content": "string", // Full markdown content
  "category": "string",
  "readTime": "string",
  "published": "boolean",
  "publishDate": "datetime",
  "createdAt": "datetime",
  "updatedAt": "datetime",
  "seoTitle": "string",
  "seoDescription": "string"
}
```

### 2. Testimonials (`testimonials`)
```json
{
  "_id": "ObjectId",
  "name": "string",
  "company": "string",
  "location": "string",
  "text": "string",
  "rating": "number",
  "published": "boolean",
  "createdAt": "datetime",
  "updatedAt": "datetime"
}
```

### 3. Contact Submissions (`contact_submissions`)
```json
{
  "_id": "ObjectId",
  "name": "string",
  "email": "string",
  "phone": "string",
  "company": "string",
  "consultationType": "string",
  "message": "string",
  "status": "string", // new, contacted, completed
  "submittedAt": "datetime",
  "notes": "string" // Admin notes
}
```

### 4. Services (`services`)
```json
{
  "_id": "ObjectId",
  "title": "string",
  "description": "string",
  "icon": "string",
  "features": ["string"],
  "pricing": {
    "basic": "string",
    "intermediate": "string", 
    "advanced": "string",
    "hourly": "string",
    "halfDay": "string",
    "fullDay": "string"
  },
  "published": "boolean",
  "order": "number",
  "updatedAt": "datetime"
}
```

### 5. Pages (`pages`)
```json
{
  "_id": "ObjectId",
  "slug": "string", // home, about, contact
  "title": "string",
  "content": "object", // Flexible content structure
  "seoTitle": "string",
  "seoDescription": "string",
  "published": "boolean",
  "updatedAt": "datetime"
}
```

### 6. Admin Users (`admin_users`)
```json
{
  "_id": "ObjectId",
  "email": "string",
  "passwordHash": "string",
  "name": "string",
  "role": "string", // admin, editor
  "lastLogin": "datetime",
  "createdAt": "datetime"
}
```

## API Endpoints

### Public Endpoints
- `GET /api/blog` - Get published blog posts (with pagination)
- `GET /api/blog/:slug` - Get single blog post by slug
- `GET /api/testimonials` - Get published testimonials
- `GET /api/services` - Get published services
- `GET /api/pages/:slug` - Get page content (home, about, etc.)
- `POST /api/contact` - Submit contact form
- `POST /api/newsletter` - Newsletter signup

### Admin Endpoints (Protected)
- `POST /api/auth/login` - Admin login
- `POST /api/auth/logout` - Admin logout
- `GET /api/auth/me` - Get current admin user

#### Blog Management
- `GET /api/admin/blog` - Get all blog posts (including drafts)
- `POST /api/admin/blog` - Create new blog post
- `PUT /api/admin/blog/:id` - Update blog post
- `DELETE /api/admin/blog/:id` - Delete blog post

#### Testimonial Management
- `GET /api/admin/testimonials` - Get all testimonials
- `POST /api/admin/testimonials` - Create testimonial
- `PUT /api/admin/testimonials/:id` - Update testimonial
- `DELETE /api/admin/testimonials/:id` - Delete testimonial

#### Contact Management
- `GET /api/admin/contacts` - Get contact submissions
- `PUT /api/admin/contacts/:id` - Update contact status/notes

#### Content Management
- `GET /api/admin/services` - Get all services
- `PUT /api/admin/services/:id` - Update service
- `GET /api/admin/pages` - Get all pages
- `PUT /api/admin/pages/:slug` - Update page content

#### Analytics
- `GET /api/admin/analytics` - Get basic analytics (contacts, blog views, etc.)

## Frontend Integration Plan

### Components to Update

#### 1. Blog Section (New Component)
- Create `BlogSection.jsx` to replace mock blog data
- Add individual blog post pages
- Implement pagination and categories

#### 2. Services Component
- Update to fetch from `/api/services`
- Remove hardcoded pricing and features

#### 3. Testimonials Component  
- Update to fetch from `/api/testimonials`
- Add loading states

#### 4. Contact Component
- Update form submission to POST to `/api/contact`
- Add success/error handling
- Implement form validation

#### 5. Admin Dashboard (New)
- Create admin login page
- Create dashboard layout with navigation
- Content management interfaces for all models
- Analytics dashboard

### Mock Data Removal
Remove the following from `mock.js`:
- `services` array → Replace with API call
- `testimonials` array → Replace with API call  
- `blogPosts` array → Replace with API call
- Contact form handling → Replace with API submission

Keep in `mock.js`:
- `hero` content (can be moved to pages later)
- `about` content (can be moved to pages later)
- `painPoints` array (static content)
- `contact` info (can be moved to environment/config)

## Authentication Strategy
- JWT-based authentication for admin users
- Protected routes using middleware
- Session management for admin dashboard
- Password hashing with bcrypt

## SEO Considerations
- Dynamic meta tags based on page content
- Structured data for local business
- Sitemap generation
- Robot.txt configuration

## Security Features
- Input validation on all endpoints
- Rate limiting on contact form
- CORS configuration
- Environment variable protection
- SQL injection prevention (using MongoDB with proper sanitization)

## GDPR Compliance
- Contact form consent checkbox
- Data retention policies
- Privacy policy page
- Cookie consent (if implementing analytics)
- Data export/deletion capabilities

## Implementation Priority
1. Database models and basic CRUD operations
2. Public API endpoints (blog, testimonials, services, contact)
3. Frontend integration with public APIs
4. Admin authentication system
5. Admin dashboard and CMS functionality
6. SEO and analytics features
7. Advanced features (newsletter, analytics dashboard)

## Testing Strategy
- Unit tests for API endpoints
- Integration tests for database operations  
- Frontend testing for form submissions
- Admin dashboard functionality testing