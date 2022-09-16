#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests


def main(dict):
    databaseName = "reviews"
    {
    "COUCH_URL":
      "https://apikey-v2-ku49dr2v78o8bg2gjaz7imt012kd4uk2o0h7rcfffan:615afb7dd49cb7dcdb71ed995f1fd8cd@0f7a2674-9824-43fc-9db6-4d91e85ccae8-bluemix.cloudantnosqldb.appdomain.cloud",
    "IAM_API_KEY": "9l_oha7Xbw-yNG5l96ccsVWD0dGQ2DQSt-RWd8DlIshM",
    "COUCH_USERNAME": "apikey-v2-ku49dr2v78o8bg2gjaz7imt012kd4uk2o0h7rcfffan",
    }

    try:
        client = Cloudant.iam(
            account_name=dict["COUCH_USERNAME"],
            api_key=dict["IAM_API_KEY"],
            connect=True,
        )
        print("Databases: {0}".format(client.all_dbs()))
    except CloudantException as ce:
        print("unable to connect")
        return {"error": ce}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    return {"dbs": client.all_dbs()}
