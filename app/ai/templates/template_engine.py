from app.ai.templates.construction_erp import template as construction
from app.ai.templates.aluminium_factory_erp import template as aluminium
from app.ai.templates.facade_erp import template as facade
from app.ai.templates.trading_erp import template as trading
from app.ai.templates.manufacturing_erp import template as manufacturing


class TemplateEngine:

    def list(self):

        return [
            construction.create(),
            aluminium.create(),
            facade.create(),
            trading.create(),
            manufacturing.create()
        ]


engine = TemplateEngine()
