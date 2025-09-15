from flask import Blueprint, request, jsonify
from db import db
from models import Topic, Skill

bp = Blueprint('api', __name__)

# -------------------- Topics --------------------
@bp.route("/topics", methods=["GET"])
def get_topics():
    # Filter per Query-Parameter
    name_filter = request.args.get("name")
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    
    query = Topic.query
    if name_filter:
        query = query.filter(Topic.name.ilike(f"%{name_filter}%"))
    
    topics_paginated = query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        "total": topics_paginated.total,
        "pages": topics_paginated.pages,
        "current_page": topics_paginated.page,
        "topics": [t.to_dict() for t in topics_paginated.items]
    })


# -------------------- Skills --------------------
@bp.route("/skills", methods=["GET"])
def get_skills():
    skills = Skill.query.all()
    return jsonify([s.to_dict() for s in skills])

@bp.route("/skills/<int:skill_id>", methods=["GET"])
def get_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    return jsonify(skill.to_dict())

@bp.route("/skills", methods=["POST"])
def create_skill():
    data = request.get_json()
    skill = Skill(name=data["name"], topic_id=data["topic_id"])
    db.session.add(skill)
    db.session.commit()
    return jsonify(skill.to_dict()), 201

@bp.route("/skills/<int:skill_id>", methods=["PUT"])
def update_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    data = request.get_json()
    skill.name = data.get("name", skill.name)
    skill.topic_id = data.get("topic_id", skill.topic_id)
    db.session.commit()
    return jsonify(skill.to_dict())

@bp.route("/skills/<int:skill_id>", methods=["DELETE"])
def delete_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    db.session.delete(skill)
    db.session.commit()
    return jsonify({"message": "Skill deleted"})

@bp.route("/skills", methods=["GET"])
def get_skills():
    # Query-Parameter
    name_filter = request.args.get("name")
    topic_filter = request.args.get("topic_id")
    sort_by = request.args.get("sort_by", "id")  # Default sortiert nach ID
    sort_order = request.args.get("sort_order", "asc")  # "asc" oder "desc"
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    
    query = Skill.query
    
    if name_filter:
        query = query.filter(Skill.name.ilike(f"%{name_filter}%"))
    if topic_filter:
        query = query.filter(Skill.topic_id == int(topic_filter))
    
    # Sortierung
    if sort_order.lower() == "desc":
        query = query.order_by(db.desc(getattr(Skill, sort_by)))
    else:
        query = query.order_by(getattr(Skill, sort_by))
    
    # Pagination
    skills_paginated = query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        "total": skills_paginated.total,
        "pages": skills_paginated.pages,
        "current_page": skills_paginated.page,
        "skills": [s.to_dict() for s in skills_paginated.items]
    })
