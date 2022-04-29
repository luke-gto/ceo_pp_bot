import pandas as pd
from src.database_handler import insert
from datetime import date


def get_poll_data(date_session, poll):

    sep = " - Il "
    poll_dict = poll.__dict__
    poll_json = poll_dict["json"]["poll"]
    question = poll_json["question"]  ###

    presenter = question.split(sep, 1)[0]
    category = "il_" + question.split(sep, 1)[1]
    total_voters = poll_json["total_voter_count"]  ###risposta al comando save
    answers = {}
    # Nel dataframe finale: presenter, category, final_score
    for item in poll_json["options"]:
        name = int(item["text"])
        answers[name] = item

    vote_dataframe = pd.DataFrame.from_dict(answers).T

    vote_dataframe = vote_dataframe.astype(int)
    final_score_cursato = vote_dataframe.prod(axis=1)  # idk why but it works
    final_score = final_score_cursato.sum()

    insert(date_session, presenter, category, int(final_score))

    return total_voters
