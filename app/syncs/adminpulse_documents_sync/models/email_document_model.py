from .email_attachment_model import EmailAttachmentModel

class EmailDocumentModel:
    def __init__(self, item: dict):
        self._id = item['id']
        self._document_id = item['documentId']
        self._created_date = item['createDate']
        self._date = item['date']
        self._subject = item['subject']
        self._from = item['from']
        self._to = item['to']
        self._cc_list = item['cc']
        self._bcc_list = item['bcc']
        self._document_url = item['documentUrl']
        
        relation_identifiers = item.get('relationIdentifiers', {})
        if len(relation_identifiers) > 1:
            raise NotImplementedError("Relation identifiers handling is not implemented yet.")
        self._relation_identifier = relation_identifiers[0] if relation_identifiers else None

        attachments = item['attachments']
        self._attachments = [EmailAttachmentModel(attachment) for attachment in attachments]
