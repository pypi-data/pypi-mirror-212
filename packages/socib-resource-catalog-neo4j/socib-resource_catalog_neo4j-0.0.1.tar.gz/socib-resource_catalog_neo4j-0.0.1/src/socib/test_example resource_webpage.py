import logging
import os
import resource
import sys

import coloredlogs

from neomodel import config
from neomodel import db

from socib.resource_catalog.namespace import SOCIB

from socib.resource_catalog.models import Base
from socib.resource_catalog.models import Concept
from socib.resource_catalog.models import Organization
from socib.resource_catalog.models import Resource
from socib.resource_catalog.models import WebPage

if "__main__" == __name__:
    logger = logging.getLogger()
    coloredlogs.install(logger=logger, level=logging.DEBUG)

    config.DATABASE_URL="neo4j://neo4j:ahm7eiNgqueigh3ZohCa4aa9Thij4gie@172.16.132.7:7687"
    #config.DATABASE_URL="neo4j+s://neo4j:9EDSrOntutZlOsRtwnzDgVHiiwOX-YSh1vmG5HaTUt0@0306c83a.databases.neo4j.io:7687"

    config.AUTO_INSTALL_LABELS = True

    Base.setModelOffline(True)

    organizationUID = Organization.findUIDByAlias(alias=["xxxxinfo@socib.es", "https://grid.ac"])
    organizationUID = Organization.findUIDByAlias(alias=["info@socib.es", "https://grid.ac"])

    #uid, rid = self.findUIDByAlias(alias=[a.uri for a in self.alias])
    #if uid is not None: self.uid = uid; self.rid=rid

    concept  = Concept()
    concept.uid = Concept.buildURI("EXAMPLES", "TEST", "CommonConcept")
    concept.name = "Common concept"
    concept.sources = ["EXAMPLE"]

    parent_resource = Resource()
    parent_resource.uid = Resource.buildURI("EXAMPLES", "TEST", "ParentMyResource")
    parent_resource.name = "Parent of My resource"
    parent_resource.sources = ["EXAMPLE"]
    parent_resource.concepts.connect(concept)

    webpage = WebPage()
    webpage.uid = Resource.buildURI("EXAMPLES", "TEST", "MyWebPage")
    webpage.name = "My webpage"
    webpage.sources = ["EXAMPLE"]

    resource = Resource()
    resource.uid = Resource.buildURI("EXAMPLES", "TEST", "MyResource")
    resource.name = "My resource"
    resource.sources = ["EXAMPLE"]

    resource.concepts.connect(concept)
    resource.translations.connect(webpage)
    resource.parent.connect(parent_resource)

    data = resource.serialize()
    logging.debug("[__main__] {}".format(data))

    resource = Base.extractResourceClassFromSerialized(data).deserialize(data)
    logging.debug("[__main__] instance: {}".format(resource))

    Base.setModelOffline(False)

    resource.save()

    resource.delete()
    parent_resource.delete()


