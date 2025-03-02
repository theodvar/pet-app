# services/__init__.py
"""
This package contains the service layer for handling business logic.
Each service module corresponds to a different resource in the application.
"""

# Example: If you want to make a logger available across services
import logging

# Configure logging for services
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
