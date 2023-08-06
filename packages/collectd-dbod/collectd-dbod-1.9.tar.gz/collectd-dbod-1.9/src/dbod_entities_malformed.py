"""
DBOD entities malformed
"""

from dbod_plugin import DbodCollectdPlugin
from dbod_instances import MalformedDbodInstance


class DbodCollectdPluginEntitiesMalformed(DbodCollectdPlugin):
    """
    Entities malformed metric:

    """
    def read(self):
        """
        Read number of malformed dbod entities
        """
        super(DbodCollectdPluginEntitiesMalformed, self).read()
        number_of_malformed = 0
        for instance in self.instances:
            if isinstance(instance, MalformedDbodInstance):
                if instance.state == "AWAITING_APPROVAL":
                    continue
                number_of_malformed += 1
        self.dispatch([number_of_malformed])


DbodCollectdPluginEntitiesMalformed()
