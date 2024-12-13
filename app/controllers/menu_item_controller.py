from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.customer import Customer
from app.models.order import Order
from app.models.menu_item import MenuItem
from app import db  # SQLAlchemy 資料庫實例