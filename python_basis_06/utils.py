def as_dict(obj):
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}