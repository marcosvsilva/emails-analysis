from process import process_history_emails
from log import generate_log
import os

from api.gmail_api import SubjectEmail, update_email
from api.database_api import Connection
from analysis import (
    TAG_SUBJECT_GESTNFE,
    TAG_SUBJECT_STACNFE,
    TAG_SUBJECT_STACCTE,
    NAME_SYSTEM_GESTNFE,
    NAME_SYSTEM_STACNFE,
    NAME_SYSTEM_STACCTE
)


def main():
    generate_log('init system!')
    db = Connection()

    tag_subject_gestnfe = os.getenv("GESTNFE_EMAIL_TAG_SUBJECT", TAG_SUBJECT_GESTNFE)
    tag_subject_stacnfe = os.getenv("STACNFE_EMAIL_TAG_SUBJECT", TAG_SUBJECT_STACNFE)
    tag_subject_staccte = os.getenv("STACCTE_EMAIL_TAG_SUBJECT", TAG_SUBJECT_STACCTE)

    name_system_gestnfe = os.getenv("GESTNFE_NAME_SYSTEM", NAME_SYSTEM_GESTNFE)
    name_system_stacnfe = os.getenv("STACNFE_NAME_SYSTEM", NAME_SYSTEM_STACNFE)
    name_system_staccte = os.getenv("STACCTE_NAME_SYSTEM", NAME_SYSTEM_STACCTE)

    subGestNFe = SubjectEmail(tag_subject_gestnfe, name_system_gestnfe)
    subStacNFe = SubjectEmail(tag_subject_stacnfe, name_system_stacnfe)
    subStacCTe = SubjectEmail(tag_subject_staccte, name_system_staccte)

    try:
        generate_log('init check tag %s.' %(name_system_gestnfe))
        messages, informations = process_history_emails(subGestNFe)
        db.insert_information(informations)
        update_email(messages)

        generate_log('init check tag %s.' %(name_system_stacnfe))
        messages, informations = process_history_emails(subStacNFe)
        db.insert_information(informations)
        update_email(messages)

        generate_log('init check tag %s.' %(name_system_staccte))
        messages, informations = process_history_emails(subStacCTe)
        db.insert_information(informations)
        update_email(messages)

        generate_log('end process!')
    except Exception as fail:
        generate_log('Process fail, fail: %s!' %(fail))

if __name__ == "__main__":
    main()
