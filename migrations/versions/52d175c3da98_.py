"""empty message

Revision ID: 52d175c3da98
Revises: 8c2a2319df7f
Create Date: 2017-06-24 18:10:36.898105

"""

# revision identifiers, used by Alembic.
revision = '52d175c3da98'
down_revision = '8c2a2319df7f'

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('event_sub_topics',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('slug', sa.String(), nullable=False),
    sa.Column('event_topic_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['event_topic_id'], ['event_topics.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('slug')
    )
    op.alter_column('events', 'sub_topic', new_column_name='event_sub_topic_id')
    op.alter_column('events_version', 'sub_topic', new_column_name='event_sub_topic_id')
    op.execute('INSERT INTO event_sub_topics(name, slug, event_topic_id) SELECT DISTINCT event_sub_topic_id, lower(replace(regexp_replace(event_sub_topic_id, \'& |,\', \'\', \'g\'), \' \', \'-\')), event_topic_id\
               FROM events where not exists (SELECT 1 FROM event_sub_topics where event_sub_topics.name=events.event_sub_topic_id) and event_sub_topic_id is not null')
    op.execute('UPDATE events SET event_sub_topic_id = (SELECT id FROM event_sub_topics WHERE event_sub_topics.name=events.event_sub_topic_id)')
    op.execute('ALTER TABLE events ALTER COLUMN event_sub_topic_id TYPE integer USING event_sub_topic_id::integer')
    op.create_foreign_key(None, 'events', 'event_sub_topics', ['event_sub_topic_id'], ['id'], ondelete='CASCADE')
    op.execute('UPDATE events_version SET event_sub_topic_id = (SELECT id FROM event_sub_topics WHERE event_sub_topics.name=events_version.event_sub_topic_id)')
    op.execute('ALTER TABLE events_version ALTER COLUMN event_sub_topic_id TYPE integer USING event_sub_topic_id::integer')
    op.execute('UPDATE event_types set slug=replace(slug, \'/\', \'-\') where slug like \'%/%\'')
    op.execute('UPDATE event_topics set slug=replace(slug, \'/\', \'-\') where slug like \'%/%\'')
    op.execute('UPDATE event_sub_topics set slug=replace(slug, \'/\', \'-\') where slug like \'%/%\'')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('events_event_sub_topic_id_fkey', 'events', type_='foreignkey')
    op.execute('ALTER TABLE events ALTER COLUMN event_sub_topic_id TYPE varchar USING event_sub_topic_id::varchar')
    op.execute('UPDATE events SET event_sub_topic_id = (SELECT name FROM event_sub_topics WHERE event_sub_topics.id=cast(events.event_sub_topic_id as int))')
    op.execute('ALTER TABLE events_version ALTER COLUMN event_sub_topic_id TYPE varchar USING event_sub_topic_id::varchar')
    op.execute('UPDATE events_version SET event_sub_topic_id = (SELECT name FROM event_sub_topics WHERE event_sub_topics.id=cast(events_version.event_sub_topic_id as int))')
    op.alter_column('events', 'event_sub_topic_id', new_column_name='sub_topic')
    op.alter_column('events_version', 'event_sub_topic_id', new_column_name='sub_topic')
    op.drop_table('event_sub_topics')
    ### end Alembic commands ###
