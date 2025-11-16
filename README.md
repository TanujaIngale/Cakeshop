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

## **Installation & Setup**

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/cake-shop.git
cd cake-shop
