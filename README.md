# Service Connect - Django REST Framework

## Overview
Service Connect is a Django REST Framework (DRF) based API that provides a platform for customers to book various services from registered employees. The system includes user authentication, service listings, employee registrations, and service bookings.

## Features
- **User Authentication**: Register, login, OTP verification, JWT authentication.
- **Profile Management**: Users can create and update their profiles.
- **Service Listings**: Admins can manage available services and sub-services.
- **Employee Registration**: Employees can register to offer services.
- **Service Booking**: Customers can book services from registered employees.
- **Pagination Support**: Implemented pagination for large datasets.

## Installation & Setup

### Prerequisites
- Python 3.x
- Django
- Django REST Framework (DRF)
- Simple JWT

### Setup Instructions
1. Clone the repository:
   ```sh
   git clone <repository-url>
   cd service-connect
   ```
2. Create a virtual environment and activate it:
   ```sh
   python -m venv env
   source env/bin/activate  # On Windows use: env\Scripts\activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Apply database migrations:
   ```sh
   python manage.py migrate
   ```
5. Run the development server:
   ```sh
   python manage.py runserver
   ```

## JWT Authentication
Service Connect uses **JWT (JSON Web Token)** for secure authentication. After login, a token is issued which must be included in the Authorization header for protected endpoints.

### Obtain Token
```sh
POST /api/token/
Content-Type: application/json
```
**Body:**
```json
{
    "email": "user@example.com",
    "password": "yourpassword"
}
```

### Refresh Token
```sh
POST /api/token/refresh/
Content-Type: application/json
```
**Body:**
```json
{
    "refresh": "your-refresh-token"
}
```

## Database Design

### **User Registration & Authentication**
- **Register Table**: Stores user credentials and role-based access.
- **OTP Table**: Handles OTP generation and verification.
- **Profile Table**: Stores additional user details post-registration.

### **Service Management**
- **Services Table**: Stores all available service categories.
- **Subservices Table**: Stores subcategories of services.

### **Employee & Booking Management**
- **Employee Registration**: Employees sign up to offer services.
- **Service Registry**: Links employees with services and pricing.
- **Service Requests**: Customers book services from registered employees.

## API Endpoints

### **User Authentication**
| Method | Endpoint | Description |
|--------|---------|-------------|
| POST | `/api/register/` | Register a new user |
| POST | `/api/login/` | Authenticate user and get JWT token |
| POST | `/api/verify-otp/` | Verify OTP and activate account |
| GET  | `/api/profile/` | Get user profile |
| PUT  | `/api/profile/update/` | Update profile details |

### **Service Management (Admin Only)**
| Method | Endpoint | Description |
|--------|---------|-------------|
| GET | `/api/services/` | Get all services (Paginated) |
| POST | `/api/services/` | Add a new service |
| PUT | `/api/services/<id>/` | Update a service |
| DELETE | `/api/services/<id>/` | Delete a service |

### **Employee Management**
| Method | Endpoint | Description |
|--------|---------|-------------|
| POST | `/api/employees/register/` | Register a new employee |
| GET | `/api/employees/` | Get all employees (Paginated) |

### **Service Booking**
| Method | Endpoint | Description |
|--------|---------|-------------|
| GET | `/api/bookings/` | Get all bookings (Paginated) |
| POST | `/api/bookings/` | Create a new booking |
| PUT | `/api/bookings/<id>/` | Update a booking |
| DELETE | `/api/bookings/<id>/` | Cancel a booking |

## Pagination
Pagination is enabled for endpoints returning large datasets. Use query parameters to navigate:

| Parameter | Description |
|-----------|-------------|
| `?page=1` | Get first page |
| `?page=2` | Get second page |

Example:
```sh
GET /api/services/?page=2
```

## Example Request & Response
### **User Registration**
**Request:**
```sh
POST /api/register/
Content-Type: application/json
```
**Body:**
```json
{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "securepass",
    "phone_number": "9876543210"
}
```

**Response:**
```json
{
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "phone_number": "9876543210",
    "role": "customer"
}
```

## License
This project is licensed under the MIT License.

