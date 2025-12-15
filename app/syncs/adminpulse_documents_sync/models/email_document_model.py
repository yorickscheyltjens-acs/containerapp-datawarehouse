from .email_attachment_model import EmailAttachmentModel

class EmailDocumentModel:
    def __init__(self, item: dict, software: str):
        self.id = item['id']
        self.document_id = item['documentId']
        self.created_date = item['createDate']
        self.date = item['date']
        self.subject = item['subject']
        self.from_address = item['from']
        self.to_address = item['to']
        self.cc_list = item['cc']
        self.bcc_list = item['bcc']
        self.document_url = item['documentUrl']
        
        relation_identifiers = item.get('relationIdentifiers', {})
        if len(relation_identifiers) > 1:
            raise NotImplementedError("Relation identifiers handling is not implemented yet.")
        self.relation_identifier = relation_identifiers[0] if relation_identifiers else None

        attachments = item['attachments']
        self.attachments = [EmailAttachmentModel(attachment) for attachment in attachments]

        self.software = software
