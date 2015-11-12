# Copyright (c) 2011-2013 Rackspace US, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from sqlalchemy import *
from migrate.changeset.constraint import ForeignKeyConstraint

meta = MetaData()

def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind=migrate_engine
    backups = Table('backup', meta, autoload=True)
    volumes = Table('volume', meta, autoload=True)

    old_v_fk = ForeignKeyConstraint([backups.c.volume_id], [volumes.c.id])
    new_v_fk = ForeignKeyConstraint([backups.c.volume_id], [volumes.c.id],
                                    onupdate='CASCADE')
    try:
        old_v_fk.drop()
        new_v_fk.create()
    except Exception:
        if migrate_engine.url.get_dialect().name.startswith('sqlite'):
            pass
        else:
            raise



def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind=migrate_engine
    backups = Table('backup', meta, autoload=True)
    volumes = Table('volume', meta, autoload=True)

    old_v_fk = ForeignKeyConstraint([backups.c.volume_id], [volumes.c.id])
    new_v_fk = ForeignKeyConstraint([backups.c.volume_id], [volumes.c.id],
                                    onupdate='CASCADE')
    try:
        new_v_fk.drop()
        old_v_fk.create()
    except Exception:
        if migrate_engine.url.get_dialect().name.startswith('sqlite'):
            pass
        else:
            raise

