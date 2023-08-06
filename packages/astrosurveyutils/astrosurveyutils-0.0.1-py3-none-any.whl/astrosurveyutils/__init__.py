from astrosurveyutils.surveys import known_surveys, known_ukirt_surveys, \
    known_vista_surveys


def get_known_survey_names():
    return [x.survey_name for x in known_surveys]


def get_survey_by_name(name):
    for survey in known_surveys:
        if survey.survey_name == name:
            return survey

    raise ValueError(f"Survey {name} is not a known survey.")


def get_known_ukirt_survey_names():
    return [x.survey_name for x in known_ukirt_surveys]


def get_known_ukirt_surveys():
    return known_ukirt_surveys


def get_known_vista_survey_names():
    return [x.survey_name for x in known_vista_surveys]


def get_known_vista_surveys():
    return known_vista_surveys
