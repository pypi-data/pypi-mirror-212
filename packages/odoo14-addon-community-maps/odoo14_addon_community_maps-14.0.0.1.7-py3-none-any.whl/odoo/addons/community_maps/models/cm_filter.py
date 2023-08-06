from odoo import models, api, fields
from odoo.tools.translate import _


class CmFilter(models.Model):
    _name = "cm.filter"

    _inherit = ["cm.slug.id.mixin"]

    # TODO: Create Mixin and color must be selection field 🙏
    _color_schema = {
        'brand': {
            'text': 'text-brand-button',
            'border': 'border-brand-base',
            'bg': 'bg-brand-button'
        },
        'black': {
            'text': 'text-gray-700',
            'border': 'border-gray-800',
            'bg': 'bg-gray-700/30'
        },
        'pink': {
            'text': 'text-pink-900',
            'border': 'border-pink-800',
            'bg': 'bg-pink-300'
        },
        'lime': {
            'text': 'text-lime-800',
            'border': 'border-lime-800',
            'bg': 'bg-lime-500'
        },
        'green': {
            'text': 'text-green-800',
            'border': 'border-green-800',
            'bg': 'bg-green-500'
        },
        'blue': {
            'text': 'text-blue-900',
            'border': 'border-blue-900',
            'bg': 'bg-blue-300'
        },
        'violet': {
            'text': 'text-violet-800',
            'border': 'border-violet-800',
            'bg': 'bg-violet-300'
        },
        'yellow': {
            'text': 'text-yellow-800',
            'border': 'border-yellow-800',
            'bg': 'bg-yellow-500'
        },
        'red': {
            'text': 'text-red-900',
            'border': 'border-red-800',
            'bg': 'bg-red-400'
        },
        'gray': {
            'textColor': 'text-neutral-800',
            'border': 'border-neutral-800',
            'bg': 'bg-neutral-400'
        },
    }

    name = fields.Char(string=_("Name"), translate=True)
    icon = fields.Char(string=_("Icon"))
    color = fields.Char(string=_("Color"))
    marker_color = fields.Char(string=_("Marker main color (hex)"))
    marker_text_color = fields.Char(string=_("Marker text color (hex)"))
    marker_bg_color = fields.Char(string=_("Marker background color (hex)"))
    marker_border_color = fields.Char(string=_("Marker border color (hex)"))
    description = fields.Char(string=_("Description"), translate=True)
    filter_group_id = fields.Many2one("cm.filter.group", string="Filter Group")
    places_mids = fields.Many2many(
        "cm.place",
        "cm_places_filters",
        "filter_id",
        "place_id",
        string=_("Related places"),
    )

    def get_datamodel_dict(self):
        datamodel = {
            "slug": self.slug_id,
            "title": self.name,
            "name": self.name,
            "group": self.filter_group_id.slug_id,
            "icon_class": None,
            "iconKey": None,
            "markerColor": {
                "markerText": self.marker_text_color,
                "markerColor": self.marker_color,
                "markerBg": self.marker_bg_color,
                "markerBorder": self.marker_border_color
            },
            "description": None,
        }
        if self.icon:
            datamodel["iconKey"] = self.icon
            datamodel["icon_class"] = self.icon.replace('_', '-')
        if self.description:
            datamodel["description"] = self.description
        return datamodel
