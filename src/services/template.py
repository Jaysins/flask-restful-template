from ..base.service import ServiceFactory
from ..models import Template


BaseTemplateService = ServiceFactory.create_service(Template)


class TemplateService(BaseTemplateService):
    """

    """
