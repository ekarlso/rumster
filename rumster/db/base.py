#    Copyright 2014 Rackspace
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#
# Copied from Octavia
from rumster.db import types

import uuid

from oslo.db.sqlalchemy import models
from oslo.utils import timeutils
import sqlalchemy as sa
from sqlalchemy.ext import declarative


class IdMixin(object):
    """Id mixin, add to subclasses that have a tenant."""
    id = sa.Column(types.UUID(), nullable=False,
                   default=lambda i: str(uuid.uuid4()),
                   primary_key=True)


class Base(models.ModelBase, IdMixin):
    def as_dict(self):
        d = {}
        for c in self.__table__.columns:
            d[c.name] = self[c.name]
        return d


BASE = declarative.declarative_base(cls=Base)
