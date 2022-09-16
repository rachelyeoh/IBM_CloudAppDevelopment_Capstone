/**
 * Get all dealerships
 */

const { CloudantV1 } = require("@ibm-cloud/cloudant");
const { IamAuthenticator } = require("ibm-cloud-sdk-core");

async function main(params) {
  params = {
    COUCH_URL:
      "https://apikey-v2-ku49dr2v78o8bg2gjaz7imt012kd4uk2o0h7rcfffan:615afb7dd49cb7dcdb71ed995f1fd8cd@0f7a2674-9824-43fc-9db6-4d91e85ccae8-bluemix.cloudantnosqldb.appdomain.cloud",
    IAM_API_KEY: "9l_oha7Xbw-yNG5l96ccsVWD0dGQ2DQSt-RWd8DlIshM",
    COUCH_USERNAME: "apikey-v2-ku49dr2v78o8bg2gjaz7imt012kd4uk2o0h7rcfffan",
  };

  const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY });
  const cloudant = CloudantV1.newInstance({
    authenticator: authenticator,
  });
  cloudant.setServiceUrl(params.COUCH_URL);
  try {
    let dbList = await cloudant.getAllDbs();
    return { dbs: dbList.result };
  } catch (error) {
    return { error: error.description };
  }
}
