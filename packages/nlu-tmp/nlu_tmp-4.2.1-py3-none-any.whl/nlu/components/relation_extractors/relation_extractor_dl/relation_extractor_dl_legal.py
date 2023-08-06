

class RelationExtractionDLLegal:
    @staticmethod
    def get_default_model():
        from sparknlp_jsl.legal.graph.relation_extraction.relation_extraction_dl import RelationExtractionDLModel
        return RelationExtractionDLModel.pretrained(name = 'redl_bodypart_direction_biobert') \
                   .setInputCols(["entities", "sentence"]) \
                   .setOutputCol("relations")


    @staticmethod
    def get_pretrained_model(name, language, bucket='clinical/models'):
        from sparknlp_jsl.legal.graph.relation_extraction.relation_extraction_dl import RelationExtractionDLModel
        return RelationExtractionDLModel.pretrained(name, language,bucket) \
            .setInputCols(["entities", "sentence"]) \
            .setOutputCol("relations")

