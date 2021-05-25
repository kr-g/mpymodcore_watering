from modapp.watering.app import router, load_generators

from modext.auto_config.ext_spec import Plugin


class Watering_app(Plugin):
    def __init__(self):
        super().__init__()
        self.caption = "modcore watering"
        self.path_spec = "modapp.watering"
        self.generators = []
        self.generators.extend(load_generators())
        #
        ## todo refactor
        # be careful :-/
        stat_rooter = self.generators[0]
        #
        self.url_caption_tuple_list = [(stat_rooter.root + "/#", None)]


app_ext = Watering_app()
