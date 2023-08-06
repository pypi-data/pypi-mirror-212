class TokenBertFinance:
    @staticmethod
    def get_default_model():
        from sparknlp_jsl.finance.token_classification.ner.finance_bert_for_token_classifier import FinanceBertForTokenClassification
        return FinanceBertForTokenClassification.pretrained() \
            .setInputCols("sentence", "token") \
            .setOutputCol("ner")

    @staticmethod
    def get_pretrained_model(name, language, bucket=None):
        from sparknlp_jsl.finance.token_classification.ner.finance_bert_for_token_classifier import FinanceBertForTokenClassification
        return FinanceBertForTokenClassification.pretrained(name, language, bucket) \
            .setInputCols("sentence", "token") \
            .setOutputCol("ner")
