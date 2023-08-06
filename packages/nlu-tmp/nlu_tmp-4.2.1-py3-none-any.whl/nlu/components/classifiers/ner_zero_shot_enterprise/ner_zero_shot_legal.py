class ZeroShotNerLegal:
    @staticmethod
    def get_default_model():
        from sparknlp_jsl.legal.token_classification.ner.zero_shot_ner import ZeroShotNerModel
        return ZeroShotNerModel().setInputCols(["sentence", "token"]) \
            .setOutputCol("zero_shot_ner") \
            .setPredictionThreshold(0.1)

    @staticmethod
    def get_pretrained_model(name, language, bucket=None):
        from sparknlp_jsl.legal.token_classification.ner.zero_shot_ner import ZeroShotNerModel
        return ZeroShotNerModel.pretrained(name, language, bucket).setInputCols(["sentence", "token"]) \
            .setOutputCol("zero_shot_ner") \
            .setPredictionThreshold(0.1)
