from alembic import op
import sqlalchemy as sa

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String, nullable=False, unique=True, index=True),
        sa.Column('hashed_password', sa.String, nullable=False)
    )

def downgrade():
    op.drop_table('users')
