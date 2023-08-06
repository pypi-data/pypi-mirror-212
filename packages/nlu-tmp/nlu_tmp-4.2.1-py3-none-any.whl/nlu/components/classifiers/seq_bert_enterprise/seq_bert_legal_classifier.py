

class SeqBertLegalClassifier:
    @staticmethod
    def get_default_model():
        from sparknlp_jsl.legal.sequence_classification.legal_bert_for_sequence_classification import LegalBertForSequenceClassification
        return LegalBertForSequenceClassification.pretrained()

    @staticmethod
    def get_pretrained_model(name, language, bucket=None):
        from sparknlp_jsl.legal.sequence_classification.legal_bert_for_sequence_classification import LegalBertForSequenceClassification
        return LegalBertForSequenceClassification.pretrained(name, language, bucket)





