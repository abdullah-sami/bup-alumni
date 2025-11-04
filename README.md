**Base URL** 
```bash
ekhononinai.com
```

## API Endpoints

### Authentication

#### Register Student
```http
POST /api/v1/register
Content-Type: application/json

{
  "username": "24230115084",
  "password": "securepass123",
  "email": "student@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "batch": "56th",
  "program": "bba",
  "bio": "Optional bio text",
  "profile_pic": "https://example.com/pic.jpg",
  "current_position": "Software Engineer",
  "current_company": "Tech Corp",
  "is_cr": false
}
```

**Response** (201 Created):
```json
{
  "message": "Registration successful",
  "user": {
    "id": 1,
    "username": "24230115084",
    "email": "student@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "student_profile": {
    "uni_id": "2021-1-60-001",
    "batch": "56th",
    "program": "bba",
    "is_cr": false,
    "is_verified": false,
    "profile_pic": "https://example.com/pic.jpg"
  }
}
```

#### Login
```http
POST /api/v1/login
Content-Type: application/json

{
  "username": "24230115084",  // Can be uni_id, email, or phone
  "password": "securepass123"
}
```

**Response** (200 OK):
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "24230115084",
    "email": "student@example.com",
    "role": "Student",
    "student_profile": {
      "first_name": "John",
      "last_name": "Doe",
      "uni_id": "2021-1-60-001",
      "batch": "56th",
      "program": "bba",
      "is_verified": false,
      "is_cr": false
    }
  }
}
```

#### Refresh Token
```http
POST /auth/token/refresh
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Logout
```http
GET /api/v1/logout
Authorization: Bearer <access_token>
```

### Student Profiles

#### List All Profiles (with Filtering)
```http
GET /api/v1/profile/
```

**Query Parameters**:
- `batch` - Filter by batch title (exact match, case-insensitive)
- `program` - Filter by program name (exact match, case-insensitive)
- `is_cr` - Filter by CR status (true/false)
- `company` - Fuzzy search by company name
- `position` - Fuzzy search by job position

**Examples**:
```http
GET /api/v1/profile/?batch=56th
GET /api/v1/profile/?program=bba&is_cr=true
GET /api/v1/profile/?company=google
GET /api/v1/profile/?batch=56th&program=bba&is_cr=false
```

**Response** (200 OK):
```json
{
  "count": 2,
  "filters": {
    "batch": "56th",
    "program": "bba",
    "is_cr": null,
    "company": null,
    "position": null
  },
  "results": [
    {
      "first_name": "John",
      "last_name": "Doe",
      "uni_id": "2021-1-60-001",
      "bio": "Bio text",
      "profile_pic": "https://example.com/pic.jpg",
      "batch": "56th",
      "program": "bba",
      "current_job_position": "Software Engineer",
      "current_company": "Tech Corp",
      "email": "student@example.com",
      "phone": "01712345678",
      "linkedin": "https://linkedin.com/in/johndoe",
      "facebook": "https://facebook.com/johndoe",
      "instagram": "https://instagram.com/johndoe",
      "is_cr": false,
      "is_verified": false
    }
  ]
}
```

#### Get Single Profile
```http
GET /api/v1/profile/{id}/
```

**Response** (200 OK):
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "uni_id": "2021-1-60-001",
  "bio": "Bio text",
  "profile_pic": "https://example.com/pic.jpg",
  "batch": "56th",
  "program": "bba",
  "current_job_position": "Software Engineer",
  "current_company": "Tech Corp",
  "email": "student@example.com",
  "phone": "01712345678",
  "linkedin": "https://linkedin.com/in/johndoe",
  "facebook": "https://facebook.com/johndoe",
  "instagram": "https://instagram.com/johndoe",
  "is_cr": false,
  "is_verified": false
}
```

#### Update Profile (Full)
```http
PUT /api/v1/profile/{id}/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "bio": "Updated bio",
  "profile_pic": "https://example.com/new-pic.jpg",
  "current_job_position": "Senior Software Engineer",
  "current_company": "New Company",
  "phone": "01712345678",
  "linkedin": "https://linkedin.com/in/johndoe",
  "facebook": "https://facebook.com/johndoe",
  "instagram": "https://instagram.com/johndoe"
}
```

#### Update Profile (Partial)
```http
PATCH /api/v1/profile/{id}/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "bio": "Updated bio only",
  "current_company": "New Company"
}
```

### Search

#### Search Students
```http
GET /api/v1/search?q=keyword
```

**Query Parameters**:
- `q` (required) - Search keyword (minimum 2 characters)

**Search Fields** (with relevance scoring):
1. University ID (exact match - highest priority)
2. First/Last name (exact, starts with, contains)
3. Email (exact, contains)
4. Phone (exact, contains)
5. Batch title/session
6. Program name
7. Company name
8. Job position
9. Bio (lowest priority)

**Example**:
```http
GET /api/v1/search?q=john
GET /api/v1/search?q=2021-1-60
GET /api/v1/search?q=software
```

**Response** (200 OK):
```json
{
  "query": "john",
  "count": 2,
  "results": [
    {
      "first_name": "John",
      "last_name": "Doe",
      "uni_id": "2021-1-60-001",
      "batch": "56th",
      "program": "bba",
      // ... rest of profile fields
    }
  ]
}
```

## Data Models

### StudentProfile
- `first_name` - Student's first name
- `last_name` - Student's last name
- `uni_id` - University ID (unique)
- `bio` - Student biography (optional)
- `profile_pic` - Profile picture URL (optional)
- `batch` - Foreign key to Batch
- `program` - Foreign key to Program
- `current_job_position` - Current job title (optional)
- `current_company` - Current company name (optional)
- `email` - Email address (unique)
- `phone` - Phone number (optional)
- `linkedin` - LinkedIn profile URL (optional)
- `facebook` - Facebook profile URL (optional)
- `instagram` - Instagram profile URL (optional)
- `is_cr` - Class Representative status (boolean)
- `is_verified` - Verification status (boolean)

### Batch
- `title` - Batch title (e.g., "56th")
- `session` - Session year (e.g., "2021-2022")

### Program
- `name` - Program name ("bba" or "mba")

### Role
- `title` - Role title

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the access token in the Authorization header:

```
Authorization: Bearer <access_token>
```

**Token Lifetimes**:
- Access Token: 24 hours
- Refresh Token: 100 days

**Multi-Field Login**: Users can log in using any of:
- University ID (username)
- Email address
- Phone number

## Error Handling

### Common Error Responses

**400 Bad Request**:
```json
{
  "message": "Registration failed",
  "errors": {
    "username": ["A user with this university ID already exists."],
    "email": ["This field is required."]
  }
}
```

**401 Unauthorized**:
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**404 Not Found**:
```json
{
  "message": "Profile not found"
}
```






** Last edited: ** 04/11/2025
