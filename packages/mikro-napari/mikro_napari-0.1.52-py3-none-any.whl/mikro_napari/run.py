from mikro_napari.widgets.main_widget import MikroNapariWidget
import napari
import argparse

from mikro_napari.widgets.sidebar.sidebar import SidebarWidget
import os
from arkitekt.builders import publicqt
from mikro_napari.manifest import identifier, version, logo


def main(**kwargs):
    os.environ["NAPARI_ASYNC"] = "1"

    viewer = napari.Viewer()

    app = publicqt(identifier, version, parent=viewer.window.qt_viewer, logo=logo)

    widget = MikroNapariWidget(viewer, app, **kwargs)
    sidebar = SidebarWidget(viewer, app, **kwargs)
    viewer.window.add_dock_widget(widget, area="left", name="Mikro")
    viewer.window.add_dock_widget(sidebar, area="right", name="Mikro")
    # viewer.add_image(astronaut(), name="astronaut")

    with app:
        napari.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config", help="Which config file to use", default="bergen.yaml", type=str
    )
    args = parser.parse_args()

    main(config_path=args.config)
