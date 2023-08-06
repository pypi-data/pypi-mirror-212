from arkitekt.builders import publicqt
from mikro_napari.widgets.main_widget import MikroNapariWidget
from mikro_napari.manifest import identifier, version, logo
import napari


class ArkitektPluginWidget(MikroNapariWidget):
    def __init__(self, viewer: napari.viewer.Viewer) -> None:
        app = publicqt(identifier=identifier, version=version, logo=logo)

        super(ArkitektPluginWidget, self).__init__(viewer, app)

        app.enter()
