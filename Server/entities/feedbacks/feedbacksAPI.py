import json
from flask import Blueprint, jsonify, request
from . import feedbacksQuery
import utilities

feedbacks_api = Blueprint('feedbacks_api', __name__)

@feedbacks_api.route("/feedbacks/<companyId>", methods=['GET'])
def get_feedbacks_api(companyId):
    result = feedbacksQuery.getFeedbacks(companyId)
    return utilities.sendResponse(result)

@feedbacks_api.route("/send-feedback/<reservationId>", methods=['POST'])
def set_feedback_api(reservationId):
    data = json.loads(request.data)
    params = {
        "reservationId": reservationId,
        "feedbackScore": data['score'],
        "feedbackMessage": data['message'] or None,
        "userId": data['userId'] or None,
    }
    result = feedbacksQuery.setFeedback(params)
    return utilities.sendResponse(result)