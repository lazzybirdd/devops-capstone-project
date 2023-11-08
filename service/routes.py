"""
Account Service

This microservice handles the lifecycle of Accounts
"""
# pylint: disable=unused-import
from flask import jsonify, request, make_response, abort, url_for   # noqa; F401
from service.models import Account
from service.common import status  # HTTP Status Codes
from . import app  # Import Flask application

import json
from flask import Response

############################################################
# Health Endpoint
############################################################
@app.route("/health")
def health():
    """Health Status"""
    return jsonify(dict(status="OK")), status.HTTP_200_OK


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return (
        jsonify(
            name="Account REST API Service",
            version="1.0",
            # paths=url_for("list_accounts", _external=True),
        ),
        status.HTTP_200_OK,
    )


######################################################################
# CREATE A NEW ACCOUNT
######################################################################
@app.route("/accounts", methods=["POST"])
def create_accounts():
    """
    Creates an Account
    This endpoint will create an Account based the data in the body that is posted
    """
    app.logger.info("Request to create an Account")
    check_content_type("application/json")
    account = Account()
    account.deserialize(request.get_json())
    account.create()
    message = account.serialize()
    # Uncomment once get_accounts has been implemented
    location_url = url_for("get_accounts", account_id=account.id, _external=True)
    #location_url = "/"  # Remove once get_accounts has been implemented
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )

######################################################################
# LIST ALL ACCOUNTS
######################################################################
@app.route("/accounts", methods=["GET"])
def list_accounts():
    """Returns a list of Accounts"""
    app.logger.info("Request to list Accounts...")

    accounts = []

    app.logger.info("Find all")
    accounts = Account.all()

    results = [account.serialize() for account in accounts]
    app.logger.info("[%s] Accounts returned", len(results))

    #RB:
    # we cannot return a list, we have to return a stinr
    # but in this scenario the header will not get application/json automatically
    # so, the workaround is to create Response object directly 
    #return json.dumps(results), status.HTTP_200_OK
    return Response(json.dumps(results),  mimetype='application/json', status=status.HTTP_200_OK)    

######################################################################
# READ AN ACCOUNT
######################################################################
@app.route("/accounts/<int:account_id>", methods=["GET"])
def get_accounts(account_id):
    """
    Reads an Account
    This endpoint will read an Account based the account_id that is requested
    """
    app.logger.info("Request to read an Account with id: %s", account_id)

    account = Account.find(account_id)
    if not account:
        abort(status.HTTP_404_NOT_FOUND, f"Account with id [{account_id}] could not be found.")

    return account.serialize(), status.HTTP_200_OK

######################################################################
# UPDATE AN EXISTING ACCOUNT
######################################################################
@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_accounts(account_id):
    """
    Updates an Account
    This endpoint will update an Account based the data in the body that is posted
    """
    app.logger.info("Request to update an Account with id: %s", account_id)

    account = Account.find(account_id)
    if not account:
        abort(status.HTTP_404_NOT_FOUND, f"Account with id [{account_id}] could not be found.")

    #print("before check content type")
    check_content_type("application/json")
    #print(f"before deserialize: {request.data}")
    account.deserialize(request.get_json())
    #print("before update")
    account.update()
    #print("after update")

    return account.serialize(), status.HTTP_200_OK


######################################################################
# DELETE AN ACCOUNT
######################################################################
@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_accounts(account_id):
    """
    Deletes an Account
    This endpoint will delete an Account based the data in the body that is posted
    """
    app.logger.info("Request to delete an Account with id: %s", account_id)

    account = Account.find(account_id)
    if not account:
        return Response("",  mimetype='application/json', status=status.HTTP_204_NO_CONTENT)    

    print("before delete")
    #account.delete()
    print("after delete")

    return Response("",  mimetype='application/json', status=status.HTTP_204_NO_CONTENT)    


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {media_type}",
    )
