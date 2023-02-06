from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import WorkModel
from schemas import WorkSchema, UpdateWorkSchema


blp = Blueprint("Works", __name__, url_prefix='/works')


@blp.route("/<int:work_id>")
class Work(MethodView):

    # @jwt_required()
    @blp.response(200, WorkSchema)
    def get(self, work_id):
        work = WorkModel.query.get_or_404(work_id)
        return work
    
    # @jwt_required()
    @blp.arguments(UpdateWorkSchema)
    @blp.response(200, WorkSchema)
    def put(self, work_data, work_id):
        work = WorkModel.query.get_or_404(work_id)
        try:
            work_code = work_data.get('code')
            if work_code is not None:
                work.code = work_code
        except:
            db.session.rollback()
            abort(500, message="Could not update work")
        else:
            db.session.commit()
        return work

    #@jwt_required()
    def delete(self, work_id):
        work = WorkModel.query.get_or_404(work_id)
        try:
            db.session.delete(work)
        except:
            db.session.rollback()
            abort(500, message="Could not delete work")
        else:
            db.session.commit()
        return {"code": 200, "status":"OK"}


@blp.route("/")
class WorkList(MethodView):
    
    # @jwt_required()
    @blp.response(200, WorkSchema(many=True))
    def get(self):
        return WorkModel.query.all()

    # @jwt_required()
    @blp.arguments(WorkSchema)
    @blp.response(201, WorkSchema)
    def post(self, work_data):
        try:
            work = WorkModel(**work_data)
            db.session.add(work)
        except:
            db.session.rollback()
            abort(500, message="Could not create work")
        else:
            db.session.commit()
        return work
    



    
