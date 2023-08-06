class ClassifierDlLegal:
    @staticmethod

    def get_default_model():
        from sparknlp_jsl.legal.sequence_classification.legal_classifier_dl import LegalClassifierDLModel
        return LegalClassifierDLModel.pretrained() \
            .setInputCols("sentence_embeddings") \
            .setOutputCol("category")

    @staticmethod
    def get_pretrained_model(name, language, bucket=None):
        from sparknlp_jsl.legal.sequence_classification.legal_classifier_dl import LegalClassifierDLModel
        return LegalClassifierDLModel.pretrained(name,language,bucket) \
            .setInputCols("sentence_embeddings") \
            .setOutputCol("category")




    @staticmethod
    def get_trainable_model():
        from sparknlp_jsl.legal.sequence_classification.legal_classifier_dl import LegalClassifierDLApproach
        return LegalClassifierDLApproach() \
            .setInputCols("sentence_embeddings") \
            .setOutputCol("category") \
            .setLabelColumn("y") \
            .setMaxEpochs(3) \
           .setEnableOutputLogs(True)

