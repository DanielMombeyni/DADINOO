import uuid


def generate_token(user):
    access_token = str(uuid.uuid4())
    refresh_token = str(uuid.uuid4())
    user.access_token = access_token
    user.refresh_token = refresh_token
    user.save()
    return {"access_token": access_token, "refresh_token": refresh_token}
