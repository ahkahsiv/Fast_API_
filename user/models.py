from fastapi import FastAPI
from tortoise.models import Model
from tortoise import Tortoise, fields

class User(Model):
    id=fields.UUIDField(pk=True)
    email=fields.CharField(50,unique=True)
    name=fields.CharField(80)
    phone=fields.CharField(10)
    password=fields.CharField(500)