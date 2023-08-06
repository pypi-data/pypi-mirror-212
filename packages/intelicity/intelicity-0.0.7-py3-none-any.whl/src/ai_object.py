class AiObject:

    object_table = {
        0:"Lombada",
        1:"Sarjetão",
        2:"Buraco",
        5: "Recomposição_asfáltica",
        9: "Boca_de_Lobo",
        10: "Sarjeta",
        16: "Lixeira",
        17: "Hidrante",
        18: "Paralelepipido",
        19: "Boca_de_Leão",
        23: "Sinalização_Horizontal",
        24: "Placa",
        25: "Fissura",
        26: "Tampa_de_Pv",
        40: "Saco_de_varrição",

        3: "Tampa_de_PV_adequada",
        4: "Tampa_de_PV_inadequada",
        6: "Fissura_Couro_de_Jacaré",
        7: "Fissura_Transversal",
        8: "Fissura_Longitudinal",
        11: "Placa_de_Regulamentação",
        12: "Placa_de_Advertência",
        13: "Placa_de_Indicação",
        14: "Placa_Educativa",
        15: "PlacaAuxiliar",
        27: "Boca_de_lobo_adequada",
        28: "Boca_de_lobo_inadequada",
        29: "Sarjetão_adequado",
        30: "Sarjetão_inadequado",
        33: "Entulho",
        34: "Faixa_de_Pedestre",
        35: "Poste",
        36: "Lixeira_Adequada",
        37: "Lixeira_Inadequada",
        38: "Lixeira_Transbordando",
        39: "Galhardete",
    }

    @classmethod
    def get_object_name_or_default(cls, ai_id: int) -> str:
        if ai_id in cls.object_table.keys():
            return cls.object_table[ai_id]
        else:
            return f"no ai object name found with id: {ai_id}"

    @classmethod
    def get_object_name(cls, ai_id : int) -> str:
        if ai_id in cls.object_table.keys():
            return cls.get_object_name_or_default(ai_id)
        else:
            raise Exception(cls.get_object_name_or_default(ai_id))

    def __init__(self, global_ai_id : int):
        self.ai_id = global_ai_id

    @classmethod
    def create_from_local_id(cls, local_object_id: int, local_root_object_id: int) -> "AiObject":
        ai_object = AiObject(local_object_id + local_root_object_id)
        return ai_object

    @classmethod
    def create_from_global_id(cls,global_object_id) -> "AiObject":
        ai_object = AiObject(global_object_id)
        return ai_object

    def get_local_id(self, local_root_object_id: int) -> int:
        return self.ai_id - local_root_object_id

    def get_global_id(self) -> int:
        return self.ai_id

    def __eq__(self, other):
        if isinstance(other, AiObject):
            return self.ai_id == other.ai_id
        else:
            return False
