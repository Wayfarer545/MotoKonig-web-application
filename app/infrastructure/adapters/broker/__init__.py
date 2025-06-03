# app/infrastructure/adapters/broker/__init__.py
from .rabbitmq import new_broker

__all__ = ["new_broker"]