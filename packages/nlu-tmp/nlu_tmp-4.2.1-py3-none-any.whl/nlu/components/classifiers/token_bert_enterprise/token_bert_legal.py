class TokenBertLegal:
    @staticmethod
    def get_default_model():
        from sparknlp_jsl.legal.token_classification.ner.legal_bert_for_token_classifier import LegalBertForTokenClassification
        return LegalBertForTokenClassification.pretrained() \
            .setInputCols("sentence", "token") \
            .setOutputCol("ner")

    @staticmethod
    def get_pretrained_model(name, language, bucket=None):
        from sparknlp_jsl.legal.token_classification.ner.legal_bert_for_token_classifier import LegalBertForTokenClassification
        return LegalBertForTokenClassification.pretrained(name, language, bucket) \
            .setInputCols("sentence", "token") \
            .setOutputCol("ner")
