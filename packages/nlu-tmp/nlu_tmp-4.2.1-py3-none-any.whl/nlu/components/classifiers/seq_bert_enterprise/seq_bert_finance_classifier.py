

class SeqBertFinanceClassifier:
    @staticmethod
    def get_default_model():
        from sparknlp_jsl.finance.sequence_classification.finance_bert_for_sequence_classification import FinanceBertForSequenceClassification
        return FinanceBertForSequenceClassification.pretrained()

    @staticmethod
    def get_pretrained_model(name, language, bucket=None):
        from sparknlp_jsl.finance.sequence_classification.finance_bert_for_sequence_classification import FinanceBertForSequenceClassification
        return FinanceBertForSequenceClassification.pretrained(name, language, bucket)





