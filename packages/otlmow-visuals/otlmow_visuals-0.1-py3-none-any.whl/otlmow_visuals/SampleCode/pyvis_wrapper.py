from otlmow_model.Classes.Onderdeel.Bevestiging import Bevestiging
from otlmow_model.Classes.Onderdeel.Verkeersregelaar import Verkeersregelaar
from otlmow_model.Classes.Onderdeel.Wegkantkast import Wegkantkast
from otlmow_model.Helpers.RelationCreator import create_relation

from otlmow_visuals.PyVisWrapper import PyVisWrapper

if __name__ == '__main__':
    vr = Verkeersregelaar()
    vr.assetId.identificator = '01'
    kast = Wegkantkast()
    kast.assetId.identificator = '02'
    bevestiging = create_relation(source=kast, target=vr, relation_type=Bevestiging)
    assets = (vr, kast, bevestiging)

    PyVisWrapper().show(assets)
