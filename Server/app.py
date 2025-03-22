from flask import Flask, redirect
from entities.account.accountAPI import account_api
from entities.activities.activitiesAPI import activities_api
from entities.filters.filtersAPI import filters_api
from entities.feedbacks.feedbacksAPI import feedbacks_api
from entities.reservations.reservationsAPI import reservations_api
from entities.rewards.rewardsAPI import rewards_api
from entities.companies.companiesAPI import companies_api

app = Flask(__name__)

app.register_blueprint(account_api)
app.register_blueprint(activities_api)
app.register_blueprint(filters_api)
app.register_blueprint(feedbacks_api)
app.register_blueprint(reservations_api)
app.register_blueprint(rewards_api)
app.register_blueprint(companies_api)

# Redirect alla pagina principale (attività)
@app.route("/")
def redirectToActivities():
    return redirect('static/activities/activities.html')