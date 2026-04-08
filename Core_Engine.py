from lex_amoris import LexAmoris
from lex_amoris.euystacio import Euystacio
from lex_amoris.core.principles import (
    COMPASSION, DIGNITY, TRUTH, BENEVOLENCE, 
    STEWARDSHIP, FORGIVENESS, RECIPROCITY, Principle
)

def setup_kosymbiosis_agent(agent_name="Euystacio"):
    # Caricamento principi core
    principles = [COMPASSION, DIGNITY, TRUTH, BENEVOLENCE, STEWARDSHIP, FORGIVENESS, RECIPROCITY]
    
    fw = LexAmoris(principles=principles)
    
    # Aggiunta principio personalizzato per il contesto Kosymbiosis
    fw.add_principle(Principle(
        name="IVBS Transparency",
        description="Ensure total biological transparency between mycelium and digital signals.",
        keywords=["mycelium", "soil", "biological", "transparency", "ivbs", "moisture"]
    ))

    return Euystacio(framework=fw, name=agent_name)
