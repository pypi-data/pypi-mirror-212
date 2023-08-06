

class ZeroShotRelationExtractorFinance:
    @staticmethod
    def get_default_model():
        from sparknlp_jsl.finance.graph.relation_extraction.zero_shot_relation_extraction import ZeroShotRelationExtractionModel
        return ZeroShotRelationExtractionModel.pretrained(name = 'redl_bodypart_direction_biobert') \
            .setInputCols(["entities", "sentence"]) \
            .setOutputCol("relations")


    @staticmethod
    def get_pretrained_model(name, language, bucket='clinical/models'):
        from sparknlp_jsl.finance.graph.relation_extraction.zero_shot_relation_extraction import ZeroShotRelationExtractionModel
        return ZeroShotRelationExtractionModel.pretrained(name, language,bucket) \
            .setInputCols(["entities", "sentence"]) \
            .setOutputCol("relations")

