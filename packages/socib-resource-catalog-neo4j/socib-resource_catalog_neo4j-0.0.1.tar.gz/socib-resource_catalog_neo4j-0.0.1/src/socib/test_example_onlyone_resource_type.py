import logging
import os
import sys

import coloredlogs

from neomodel import config
from neomodel import db

from socib.resource_catalog.namespace import SOCIB

from socib.resource_catalog.models import Base
from socib.resource_catalog.models import Person

if "__main__" == __name__:
    logger = logging.getLogger()
    coloredlogs.install(logger=logger, level=logging.DEBUG)

    config.DATABASE_URL="neo4j://neo4j:ahm7eiNgqueigh3ZohCa4aa9Thij4gie@172.16.132.7:7687"
    config.AUTO_INSTALL_LABELS = True

    Base.setModelOffline(True)

    uid0 = Person.buildURI("TEST", "PERSON#0")
    person0 = Person() 
    person0.uid = uid0
    person0.name = "My person name (0)"
    person0.email = "parentofnobody@people.com"
    person0.sources = ["TEST", "EXAMPLE"]

    uid1 = Person.buildURI("TEST","PERSON#1")
    person1 = Person.nodes.get_or_none(uid=uid1)
    person1 = Person() 
    person1.uid = uid1
    person1.name = "My person name (1)"
    person1.description = "My person name (1)"
    person1.email = "nobody@people.com"
    person1.sources = ["TEST", "EXAMPLE"]
    person1.parent.connect(person0)

    uid2 = Person.buildURI("TEST","PERSON#2")
    person2 = Person.nodes.get_or_none(uid=uid2)
    person2 = Person() 
    person2.uid = uid2
    person2.name = "My person name (2)"
    person2.description = "My person name (2)"
    person2.email = "nobody@people.com"
    person2.sources = ["TEST", "EXAMPLE"]
    person2.parent.connect(person0)

    uid3 = Person.buildURI("TEST","PERSON#3")
    person3 = Person.nodes.get_or_none(uid=uid3)
    person3 = Person() 
    person3.uid = uid3
    person3.name = "My person name (3)"
    person3.description = "My person name (3)"
    person3.email = "nobody@people.com"
    person3.sources = ["TEST", "EXAMPLE"]
    person3.parent.connect(person0)

    person3.alias.connect(person3.scaffold, {"uri": "https://example.org/ns#person3.1"})
    person3.alias.connect(person3.scaffold, {"uri": "https://example.org/ns#person3.2"})

    a = [a for a in person3.alias]
    a = [person3.alias.all_relationships(a) for a in person3.alias]

    person3.related.connect(person1, {"type": "IS_KNOWNS"})
    person3.related.connect(person2, {"type": "IS_UNKWONS"})

    data = person3.serialize()
    logging.debug("[__main__] {}".format(data))

    person = Person.deserialize(data)
    logging.debug("[__main__] instance: {}".format(person))

    Base.setModelOffline(False)
    logging.debug("[__main__] offline mode: {}".format(Base.getModelOffline()))
    logging.debug("[__main__] \t offline mode (person0): {}".format(person0.currentModelOffline))
    logging.debug("[__main__] \t offline mode (person1): {}".format(person1.currentModelOffline))
    logging.debug("[__main__] \t offline mode (person2): {}".format(person2.currentModelOffline))
    logging.debug("[__main__] \t offline mode (person3): {}".format(person3.currentModelOffline))

    with db.transaction:
        person3.save()

    logging.debug("[__main__] offline mode: {}".format(Base.getModelOffline()))
    logging.debug("[__main__] \t offline mode (person0): {}".format(person0.currentModelOffline))
    logging.debug("[__main__] \t offline mode (person1): {}".format(person1.currentModelOffline))
    logging.debug("[__main__] \t offline mode (person2): {}".format(person2.currentModelOffline))
    logging.debug("[__main__] \t offline mode (person3): {}".format(person3.currentModelOffline))

    with db.transaction:
        person3.delete()
        person2.delete()
        person1.delete()
        person0.delete()


