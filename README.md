# API Documentation

**Base URL** 
```bash
https://innoversebd.bdix.cloud/bup
```

## API Endpoints

### Authentication

#### Register Student
```http
POST /api/v1/register
Content-Type: application/json

{
  "username": "24230115084",
  "password": "securepass123", //required
  "email": "student@example.com", //required
  "first_name": "John", //required
  "last_name": "Doe", //required
  "batch": "56th", //required
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
    "uni_id": "24230115084",
    "batch": "56th",
    "program": "bba",
    "is_cr": false,
    "is_verified": false,
    "profile_pic": "https://example.com/pic.jpg"
  }
}
```

**Error Response** (400 Bad Request):
```json
{
  "message": "Registration failed",
  "errors": {
    "username": ["A user with this university ID already exists."],
    "email": ["A user with this email already exists."]
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
    "role": "Student",  // or "CR" if is_cr is true
    "student_profile": {
      "first_name": "John",
      "last_name": "Doe",
      "uni_id": "24230115084",
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

**Response** (200 OK):
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Logout
```http
GET /api/v1/logout
Authorization: Bearer <access_token>
```

**Response**: Redirects to login page and blacklists the access token.

---

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
GET /api/v1/profile/
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
      "id": 1,
      "first_name": "John",
      "last_name": "Doe",
      "uni_id": "24230115084",
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
  "id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "uni_id": "24230115084",
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

**Error Response** (404 Not Found):
```json
{
  "message": "Profile not found"
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

**Note**: `uni_id` and `is_verified` are read-only fields and cannot be updated.

**Response** (200 OK):
```json
{
    "id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "uni_id": "najib2@gmail.com",
    "bio": "Updated bio",
    "profile_pic": "https://example.com/new-pic.jpg",
    "batch": "GEN15",
    "program": "bba",
    "current_job_position": "Senior Software Engineer",
    "current_company": "New Company",
    "email": "najib2@gmail.com",
    "phone": "01712345678",
    "linkedin": "https://linkedin.com/in/johndoe",
    "facebook": "https://facebook.com/johndoe",
    "instagram": "https://instagram.com/johndoe",
    "is_cr": false,
    "is_verified": false
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

**Response** (200 OK):
```json
{
  "id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "uni_id": "najib2@gmail.com",
    "bio": "Updated bio",
    "profile_pic": "https://example.com/new-pic.jpg",
    "batch": "GEN15",
    "program": "bba",
    "current_job_position": "Senior Software Engineer",
    "current_company": "New Company",
    "email": "najib2@gmail.com",
    "phone": "01712345678",
    "linkedin": "https://linkedin.com/in/johndoe",
    "facebook": "https://facebook.com/johndoe",
    "instagram": "https://instagram.com/johndoe2",
    "is_cr": false,
    "is_verified": false
}
```

**Error Response** (400 Bad Request):
```json
{
  "field_name": ["Error message"]
}
```

---

### Search

#### Search Students
```http
GET /api/v1/search?q=keyword
```

**Query Parameters**:
- `q` (required) - Search keyword (minimum 2 characters)

**Search Fields** (with relevance scoring):
1. University ID (exact match - highest priority: 100)
2. First/Last name (exact: 90, starts with: 80, contains: 50)
3. Email (exact: 70, contains: 25)
4. Phone (exact: 65, contains: 25)
5. Batch title/session (40)
6. Program name (35)
7. Company name (30)
8. Job position (30)
9. Bio (lowest priority: 10)

Results are ordered by relevance score, then by first and last name. Limited to 50 results.

**Examples**:
```http
GET /api/v1/search?q=john
GET /api/v1/search?q=24230115084
GET /api/v1/search?q=software
GET /api/v1/search?q=56th
```

**Response** (200 OK):
```json
{
  "query": "john",
  "count": 2,
  "results": [
    {
      "id": 1,
      "first_name": "John",
      "last_name": "Doe",
      "uni_id": "24230115084",
      "batch": "56th",
      "program": "bba",
      "bio": "Bio text",
      "profile_pic": "https://example.com/pic.jpg",
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

**Response for short query** (200 OK):
```json
{
  "message": "Search query must be at least 2 characters",
  "results": []
}
```

**Response for empty query** (200 OK):
```json
{
  "message": "Please provide a search query",
  "results": []
}
```

---

### Admin - Student Verification

#### List Unverified Profiles
```http
GET /api/v1/admin/verify/
Authorization: Bearer <access_token>
```

**Response** (200 OK):
```json
[
    {
        "id": 2,
        "first_name": "Raiyana",
        "last_name": "Noor",
        "uni_id": "24230115136",
        "bio": "Abeder Crush.",
        "profile_pic": "http://example.com/profile.jpg",
        "batch": "GEN15",
        "program": "bba",
        "current_job_position": "Student",
        "current_company": "BOOP",
        "email": "raiyana@gmail.com",
        "phone": null,
        "linkedin": null,
        "facebook": null,
        "instagram": null,
        "is_cr": false,
        "is_verified": false
    }
]
```

#### Verify Student Profile
```http
POST /api/v1/admin/verify/{id}/verify/
Authorization: Bearer <access_token>
```

**Response** (200 OK):
```json
{
    "message": "Profile verified successfully",
    "profile": {
        "id": 3,
        "first_name": "Raiyana",
        "last_name": "Noor",
        "uni_id": "raiyana2@gmail.com",
        "bio": null,
        "profile_pic": null,
        "batch": "GEN15",
        "program": "bba",
        "current_job_position": null,
        "current_company": null,
        "email": "raiyana2@gmail.com",
        "phone": null,
        "linkedin": null,
        "facebook": null,
        "instagram": null,
        "is_cr": false,
        "is_verified": true
    }
}
```

**Error Response** (404 Not Found):
```json
{
  "message": "Profile not found"
}
```

---

## Data Models

### StudentProfile
- `id` - Primary key (auto-generated)
- `first_name` - Student's first name (max 30 chars)
- `last_name` - Student's last name (max 30 chars)
- `uni_id` - University ID (max 20 chars, unique)
- `bio` - Student biography (optional, text)
- `profile_pic` - Profile picture URL (optional)
- `batch` - Foreign key to Batch
- `program` - Foreign key to Program
- `current_job_position` - Current job title (optional, max 200 chars)
- `current_company` - Current company name (optional, max 200 chars)
- `email` - Email address (unique, required)
- `phone` - Phone number (optional, max 15 chars)
- `linkedin` - LinkedIn profile URL (optional)
- `facebook` - Facebook profile URL (optional)
- `instagram` - Instagram profile URL (optional)
- `is_cr` - Class Representative status (boolean, default: false)
- `is_verified` - Verification status (boolean, default: false)

**Read-only fields**: `uni_id`, `is_verified`

### Batch
- `title` - Batch title (e.g., "56th")
- `session` - Session year (e.g., "2021-2022")

### Program
- `name` - Program name (e.g., "bba", "mba")

### Role
- `title` - Role title

---

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the access token in the Authorization header:

```
Authorization: Bearer <access_token>
```

**Token Lifetimes**:
- Access Token: 24 hours
- Refresh Token: 100 days

**Token Rotation**: 
- `ROTATE_REFRESH_TOKENS`: False
- `BLACKLIST_AFTER_ROTATION`: True

**Multi-Field Login**: Users can log in using any of:
- University ID (username)
- Email address
- Phone number

The custom authentication backend (`MultiFieldAuthBackend`) automatically determines which field is being used.

---

## Permissions

### Public Endpoints (No Authentication Required)
- `POST /api/v1/register` - Student registration
- `POST /api/v1/login` - User login
- `POST /auth/token/refresh` - Token refresh
- `GET /api/v1/profile/` - List all profiles
- `GET /api/v1/profile/{id}/` - Get single profile
- `GET /api/v1/search` - Search students

### Protected Endpoints (Authentication Required)
- `PUT /api/v1/profile/{id}/` - Update profile (full)
- `PATCH /api/v1/profile/{id}/` - Update profile (partial)
- `GET /api/v1/logout` - Logout
- `GET /api/v1/admin/verify/` - List unverified profiles
- `POST /api/v1/admin/verify/{id}/verify/` - Verify profile

---

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

**500 Internal Server Error**:
```json
{
  "detail": "Internal server error"
}
```

---

## Features

### Smart Search
- Multi-field search with relevance scoring
- Searches across: name, uni_id, email, phone, batch, program, company, position, bio
- Results ordered by relevance
- Minimum query length: 2 characters
- Maximum results: 50

### Flexible Filtering
- Filter by batch, program, CR status
- Fuzzy search by company and position
- Combine multiple filters
- Results ordered by CR status first, then alphabetically

### User Roles
- **Student**: Regular student user
- **CR (Class Representative)**: Student with CR privileges
- Role automatically determined based on `is_cr` field

### Verification System
- New students are unverified by default (`is_verified: false`)
- Admin can verify students through verification endpoint
- List all unverified profiles for review

---

## CORS Configuration

- **CORS Enabled**: Yes
- **Allowed Origins**: All (`CORS_ALLOW_ALL_ORIGINS = True`)
- **Note**: Should be restricted in production

---

## Database

**Current**: SQLite3
**Location**: `backend/db.sqlite3`

---

## Notes

1. **Username vs uni_id**: The `username` in the User model stores the `uni_id` value
2. **Email/Phone Login**: The custom authentication backend handles lookups in both User and StudentProfile models
3. **Profile Updates**: `uni_id` and `is_verified` cannot be updated through the API
4. **Search Optimization**: Uses `select_related()` to reduce database queries
5. **Token Blacklisting**: Logout functionality blacklists tokens for security

---

**Last edited**: 07/11/2025
