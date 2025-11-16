# 🍰 Cake Shop Web Application

A full-stack web application for managing a bakery's cake catalog, orders, and billing. Built with **Python (Flask)**, **SQLite**, and **Bootstrap**, this project allows users to browse cakes, manage a shopping cart, checkout orders, and download PDF bills. Admins can manage cakes and view all orders through a secure dashboard.

---

## **Features**

### User Features
- User registration and login
- Browse cakes with name, price, and image
- Add cakes to shopping cart
- Checkout with automatic total calculation

### Admin Features
- Secure admin login
- Add new cakes (with optional image upload)
- Edit and delete cakes
- View all orders
- Download printable PDF bills for orders

### Technical Features
- Flask backend with session management
- SQLite database for users, admins, cakes, and orders
- PDF bill generation using `reportlab`
- Dynamic templates using Jinja2
- Secure image uploads

---
<img width="1366" height="642" alt="cake" src="https://github.com/user-attachments/assets/29f4364c-ca23-46da-86a6-2e58ad0f60ec" />
<img width="1366" height="634" alt="admin dashboard" src="https://github.com/user-attachments/assets/67c308ca-1d8f-4fbc-a7a3-44ed1b5b8a28" />
<img width="1366" height="636" alt="user login" src="https://github.com/user-attachments/assets/3b5ca01d-2d78-4fed-971c-5a22fe274d6a" />
<img width="1366" height="629" alt="registration" src="https://github.com/user-attachments/assets/c05ea991-c9ba-488d-8b63-f07fa2542555" />
<img width="1366" height="641" alt="cart" src="https://github.com/user-attachments/assets/d033679a-c43e-4ef5-8367-7fa471f4fe7f" />
<img width="420" height="333" alt="bill" src="https://github.com/user-attachments/assets/e959a0b6-ecdb-4f5c-b2c7-28fe13103e23" />

## **Installation & Setup**

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/cake-shop.git
cd cake-shop
