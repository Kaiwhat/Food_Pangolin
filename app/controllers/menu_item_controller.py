from flask import Blueprint, render_template, request, redirect, url_for, flash
import app.models.customer as Customer
import app.models.order as Order
import app.models.menu_item as MenuItem
from app import db  # SQLAlchemy 資料庫實例