import json
import logging

import azure.functions as func

from config import SUMMARY_FILE


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Processing Summary Request")

    try:
        with open(SUMMARY_FILE, "r", encoding="utf-8") as file:
            summaries = json.load(file)

        return func.HttpResponse(
            json.dumps(summaries),
            mimetype="application/json",
            status_code=200,
        )

    except Exception as e:
        return func.HttpResponse(
            str(e),
            status_code=500,
        )
