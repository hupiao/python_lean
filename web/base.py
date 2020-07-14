# -*- coding: utf-8 -*-

from flask import Blueprint


class SanboxBlueprint(Blueprint):
    warn_on_modifications = False
    _got_registered_once = False

    def __init__(self, *args, **kwargs):
        self.blueprint_members = []
        super(SanboxBlueprint, self).__init__(*args, **kwargs)

    def register_bp(self, blueprint):
        if blueprint.url_prefix is None:
            blueprint.url_prefix = self.url_prefix
        else:
            blueprint.url_prefix = self.url_prefix + blueprint.url_prefix
            if isinstance(blueprint, SanboxBlueprint):
                for member in blueprint.blueprint_members:
                    member.url_prefix = blueprint.url_prefix

        self.blueprint_members.append(blueprint)
