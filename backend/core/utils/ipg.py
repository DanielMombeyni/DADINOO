"""
Image path Generators.
"""

import os
import uuid


def document_image_file_path(instance, file_name):
    """Generate file path for new document image."""
    ext = os.path.splitext(file_name)[1]
    file_name = f"{uuid.uuid4()}{ext}"
    return os.path.join("uploads", "document", file_name)


def profile_image_file_path(instance, file_name):
    """Generate file path for new profile image."""
    ext = os.path.splitext(file_name)[1]
    file_name = f"{uuid.uuid4()}{ext}"
    return os.path.join("uploads", "profile", file_name)


def game_image_file_path(instance, file_name):
    """Generate file path for new profile image."""
    ext = os.path.splitext(file_name)[1]
    file_name = f"{uuid.uuid4()}{ext}"
    return os.path.join("uploads", "game", file_name)


def category_image_file_path(instance, file_name):
    """Generate file path for new profile image."""
    ext = os.path.splitext(file_name)[1]
    file_name = f"{uuid.uuid4()}{ext}"
    return os.path.join("uploads", "category", file_name)
