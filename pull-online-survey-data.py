import argparse
import json
import firebase_admin
from firebase_admin import credentials, firestore
import firebase_admin.auth
from google.cloud.firestore_v1 import DocumentReference
import pandas as pd


def export_user_survey_to_excel(serviceAccountKeyPath: str, excelFileName: str) -> None:
    cred = credentials.Certificate(serviceAccountKeyPath)
    app = firebase_admin.initialize_app(cred, {"databaseURL": "-default"})

    database = firestore.client()
    records = []

    for doc_ref in database.collection("userSurvey").list_documents():
        doc_ref: DocumentReference
        records.append(doc_ref.get().to_dict())

    pd.DataFrame.from_records(records).to_excel(excelFileName)

    firebase_admin.delete_app(app)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--serviceAccountKeyPath",
        "-p",
        type=str,
        help="The path to the service account key",
        required=True,
    )

    parser.add_argument(
        "--filePath",
        "-f",
        type=str,
        help="The file the user survey data is exported to. Must be a .xlsx file.",
        required=True,
    )

    parsed_args = parser.parse_args()
    export_user_survey_to_excel(parsed_args.serviceAccountKeyPath, parsed_args.filePath)
