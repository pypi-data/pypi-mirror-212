import os


def get_pqa_key():
    try:
        return os.environ["PQA_API_KEY"]
    except KeyError:
        raise Exception("PQA_API_KEY environment variable not set")
