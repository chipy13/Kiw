from experta import *

class SkinFact(Fact):
    """Fact representing a skin symptom"""
    pass

class SkinDiagnosisEngine(KnowledgeEngine):
    @DefFacts()
    def _initial_action(self):
        yield Fact(action="diagnose_skin")

    # Rules for determining skin type
    @Rule(Fact(action='diagnose_skin'),
          SkinFact(oiliness='very_oily'),
          SkinFact(acne='frequent'),
          SkinFact(pores='large'),
          SkinFact(shine='quick'),
          NOT(SkinFact(sensitivity='high')))
    def oily_skin(self):
        self.declare(Fact(skin_type="Oily"))
        
    @Rule(Fact(action='diagnose_skin'),
          SkinFact(oiliness='dry'),
          SkinFact(flaking='yes'),
          SkinFact(tightness='often'),
          SkinFact(redness='sometimes'))
    def dry_skin(self):
        self.declare(Fact(skin_type="Dry"))
        
    @Rule(Fact(action='diagnose_skin'),
          SkinFact(oiliness='combination'),
          OR(SkinFact(t_zone='oily'), SkinFact(t_zone='normal')),
          OR(SkinFact(cheeks='dry'), SkinFact(cheeks='normal')))
    def combination_skin(self):
        self.declare(Fact(skin_type="Combination"))
        
    @Rule(Fact(action='diagnose_skin'),
          SkinFact(oiliness='normal'),
          SkinFact(sensitivity='low'),
          SkinFact(acne='rare'),
          SkinFact(pores='small'))
    def normal_skin(self):
        self.declare(Fact(skin_type="Normal"))
        
    @Rule(Fact(action='diagnose_skin'),
          SkinFact(sensitivity='high'),
          SkinFact(redness='often'),
          SkinFact(irritation='frequent'))
    def sensitive_skin(self):
        self.declare(Fact(skin_type="Sensitive"))

    # Product recommendations based on skin type
    @Rule(Fact(skin_type="Oily"))
    def oily_recommendations(self):
        self.declare(Fact(recommendations=[
            "Oil-free cleanser with salicylic acid",
            "Alcohol-free toner",
            "Lightweight, oil-free moisturizer",
            "Clay mask 1-2 times per week",
            "Non-comedogenic sunscreen"
        ]))
        
    @Rule(Fact(skin_type="Dry"))
    def dry_recommendations(self):
        self.declare(Fact(recommendations=[
            "Cream-based cleanser",
            "Hydrating toner with hyaluronic acid",
            "Rich moisturizer with ceramides",
            "Facial oil for extra hydration",
            "Gentle exfoliator 1-2 times per week"
        ]))
        
    @Rule(Fact(skin_type="Combination"))
    def combination_recommendations(self):
        self.declare(Fact(recommendations=[
            "Gentle foaming cleanser",
            "Balancing toner",
            "Light moisturizer for T-zone, richer for cheeks",
            "Exfoliate 1-2 times per week",
            "Oil-free sunscreen"
        ]))
        
    @Rule(Fact(skin_type="Normal"))
    def normal_recommendations(self):
        self.declare(Fact(recommendations=[
            "Gentle cleanser",
            "Hydrating toner",
            "Lightweight moisturizer",
            "Weekly exfoliation",
            "Broad-spectrum sunscreen"
        ]))
        
    @Rule(Fact(skin_type="Sensitive"))
    def sensitive_recommendations(self):
        self.declare(Fact(recommendations=[
            "Fragrance-free, gentle cleanser",
            "Soothing toner with aloe vera",
            "Hypoallergenic moisturizer",
            "Mineral-based sunscreen",
            "Avoid harsh exfoliants"
        ]))
