import json
from flask import Blueprint, jsonify, request
from . import rewardsQuery
import utilities

rewards_api = Blueprint('rewards_api', __name__)

@rewards_api.route("/rewards", methods=['GET'])
def get_rewards_api():
    result = rewardsQuery.getRewards()
    return utilities.sendResponse(result)

@rewards_api.route("/redeemed-rewards", methods=['GET'])
def redeemed_rewards_api():
    userId = request.args.get('userId') or None
    if (userId is None):
        result = []
    else:
        result = rewardsQuery.getRedeemedRewards(userId)
    return utilities.sendResponse(result)

@rewards_api.route("/user-points", methods=['GET'])
def user_points_api():
    userId = request.args.get('userId') or None
    if (userId is None):
        result = {
            "points": 0
        }
    else:
        result = rewardsQuery.getUserPoints(userId)
    return utilities.sendResponse(result)

@rewards_api.route("/redeem-reward", methods=['POST'])
def redeem_reward_api():
    data = json.loads(request.data)
    rewardId = data['rewardId'] or None
    userId = data['userId'] or None
    if (userId is None or rewardId is None):
        result = None
    else:
        result = rewardsQuery.redeemReward(userId, rewardId)
    return utilities.sendResponse(result)
