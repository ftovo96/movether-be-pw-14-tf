import json
from flask import Blueprint, jsonify, request
from . import companiesQuery
import utilities

companies_api = Blueprint('companies_api', __name__)

@companies_api.route("/companies", methods=['GET'])
def get_companies_api():
    result = companiesQuery.getCompanies()
    return utilities.sendResponse(result)

@companies_api.route("/companies/<companyId>", methods=['GET'])
def get_company_api(companyId):
    result = companiesQuery.getCompany(companyId)
    return utilities.sendResponse(result)
