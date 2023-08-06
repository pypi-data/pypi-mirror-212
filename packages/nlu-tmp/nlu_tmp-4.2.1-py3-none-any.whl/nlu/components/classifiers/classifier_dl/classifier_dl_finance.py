class ClassifierDlFinance:
    @staticmethod

    def get_default_model():
        from sparknlp_jsl.finance.sequence_classification.finance_classifier_dl import FinanceClassifierDLModel
        return FinanceClassifierDLModel.pretrained() \
            .setInputCols("sentence_embeddings") \
            .setOutputCol("category")

    @staticmethod
    def get_pretrained_model(name, language, bucket=None):
        from sparknlp_jsl.finance.sequence_classification.finance_classifier_dl import FinanceClassifierDLModel
        return FinanceClassifierDLModel.pretrained(name,language,bucket) \
            .setInputCols("sentence_embeddings") \
            .setOutputCol("category")




    @staticmethod
    def get_trainable_model():
        from sparknlp_jsl.finance.sequence_classification.finance_classifier_dl import FinanceClassifierDLApproach
        return FinanceClassifierDLApproach() \
            .setInputCols("sentence_embeddings") \
            .setOutputCol("category") \
            .setLabelColumn("y") \
            .setMaxEpochs(3) \
            .setEnableOutputLogs(True)

