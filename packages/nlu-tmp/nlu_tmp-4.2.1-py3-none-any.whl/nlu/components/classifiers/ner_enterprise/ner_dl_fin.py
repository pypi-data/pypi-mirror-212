
class NERDLFinance:
    @staticmethod
    def get_default_model():
        from sparknlp_jsl.finance.token_classification.ner.finance_ner import FinanceNerModel
        return FinanceNerModel.pretrained(name='ner_dl_bert', lang='en') \
            .setInputCols(["sentence", "token", "word_embeddings"]) \
            .setOutputCol("ner") \
            .setIncludeConfidence(True)



    @staticmethod
    def get_pretrained_model(name, language, bucket=None):
        from sparknlp_jsl.finance.token_classification.ner.finance_ner import FinanceNerModel
        return FinanceNerModel.pretrained(name,language,bucket) \
            .setInputCols(["sentence", "token", "word_embeddings"]) \
            .setOutputCol("ner") \
            .setIncludeConfidence(True)

    @staticmethod
    def get_default_trainable_model():
        from sparknlp_jsl.finance.token_classification.ner.finance_ner import FinanceNerApproach
        return FinanceNerApproach() \
            .setInputCols(["sentence", "token", "word_embeddings"]) \
            .setLabelColumn("y") \
            .setOutputCol("ner") \
            .setMaxEpochs(2) \
            .setVerbose(0) \
            .setIncludeConfidence(True)