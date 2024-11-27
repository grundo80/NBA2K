"""Add individual columns for attributes and badges in PlayerTargets

Revision ID: a02e191f95cd
Revises: 81e02bb9ce98
Create Date: 2024-10-08 14:03:17.530777

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = 'a02e191f95cd'
down_revision = '81e02bb9ce98'
branch_labels = None
depends_on = None

# Replace old player_targets with new table structure
def upgrade():
    # Drop both new_player_targets and player_targets tables if they exist
    op.execute('DROP TABLE IF EXISTS new_player_targets')
    op.execute('DROP TABLE IF EXISTS player_targets')

    # Step 1: Create the new player_targets table with individual columns
    op.create_table(
        'player_targets',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('player_id', sa.Integer(), sa.ForeignKey('player.id'), nullable=False),
        
        # Attributes
        sa.Column('acceleration', sa.Integer(), nullable=False, default=99),
        sa.Column('agility', sa.Integer(), nullable=False, default=99),
        sa.Column('ball_handle', sa.Integer(), nullable=False, default=99),
        sa.Column('block', sa.Integer(), nullable=False, default=99),
        sa.Column('defensive_consistency', sa.Integer(), nullable=False, default=99),
        sa.Column('defensive_rebound', sa.Integer(), nullable=False, default=99),
        sa.Column('draw_foul', sa.Integer(), nullable=False, default=99),
        sa.Column('driving_dunk', sa.Integer(), nullable=False, default=99),
        sa.Column('free_throw', sa.Integer(), nullable=False, default=99),
        sa.Column('hands', sa.Integer(), nullable=False, default=99),
        sa.Column('help_defense_iq', sa.Integer(), nullable=False, default=99),
        sa.Column('hustle', sa.Integer(), nullable=False, default=99),
        sa.Column('intangibles', sa.Integer(), nullable=False, default=99),
        sa.Column('interior_defense', sa.Integer(), nullable=False, default=99),
        sa.Column('lateral_quickness', sa.Integer(), nullable=False, default=99),
        sa.Column('layup', sa.Integer(), nullable=False, default=99),
        sa.Column('mid_range_shot', sa.Integer(), nullable=False, default=99),
        sa.Column('offensive_consistency', sa.Integer(), nullable=False, default=99),
        sa.Column('offensive_rebound', sa.Integer(), nullable=False, default=99),
        sa.Column('overall_durability', sa.Integer(), nullable=False, default=99),
        sa.Column('pass_accuracy', sa.Integer(), nullable=False, default=99),
        sa.Column('pass_iq', sa.Integer(), nullable=False, default=99),
        sa.Column('pass_perception', sa.Integer(), nullable=False, default=99),
        sa.Column('pass_vision', sa.Integer(), nullable=False, default=99),
        sa.Column('perimeter_defense', sa.Integer(), nullable=False, default=99),
        sa.Column('post_control', sa.Integer(), nullable=False, default=99),
        sa.Column('post_fade', sa.Integer(), nullable=False, default=99),
        sa.Column('post_hook', sa.Integer(), nullable=False, default=99),
        sa.Column('shot_iq', sa.Integer(), nullable=False, default=99),
        sa.Column('standing_dunk', sa.Integer(), nullable=False, default=99),
        sa.Column('speed', sa.Integer(), nullable=False, default=99),
        sa.Column('speed_with_ball', sa.Integer(), nullable=False, default=99),
        sa.Column('stamina', sa.Integer(), nullable=False, default=99),
        sa.Column('steal', sa.Integer(), nullable=False, default=99),
        sa.Column('strength', sa.Integer(), nullable=False, default=99),
        sa.Column('three_point_shot', sa.Integer(), nullable=False, default=99),
        sa.Column('vertical', sa.Integer(), nullable=False, default=99),
        
        # Badges
        sa.Column('aerial_wizard', sa.String(50), nullable=False, default="Hall of Fame"),
        sa.Column('ankle_assassin', sa.String(50), nullable=False, default="Hall of Fame"),
        sa.Column('bail_out', sa.String(50), nullable=False, default="Hall of Fame"),
        sa.Column('boxout_beast', sa.String(50), nullable=False, default="Hall of Fame"),
        sa.Column('break_starter', sa.String(50), nullable=False, default="Hall of Fame"),
        sa.Column('brick_wall', sa.String(50), nullable=False, default="Hall of Fame"),
        sa.Column('challenger', sa.String(50), nullable=False, default="Hall of Fame"),
        sa.Column('deadeye', sa.String(50), nullable=False, default="Hall of Fame"),
        sa.Column('dimer', sa.String(50), nullable=False, default="Hall of Fame"),
        sa.Column('float_game', sa.String(50), nullable=False, default="Hall of Fame"),
        sa.Column('glove', sa.String(50), nullable=False, default="Hall of Fame"),
        sa.Column('handles_for_days', sa.String(50), nullable=False, default="Hall of Fame"),
        sa.Column('high_flying_denier', sa.String(50), nullable=False, default="Hall of Fame"),
        sa.Column('hook_specialist', sa.String(50), nullable=False, default="Hall of Fame"),
        sa.Column('immovable_enforcer', sa.String(50), nullable=False, default="Hall of Fame"),
        sa.Column('interceptor', sa.String(50), nullable=False, default="Hall of Fame"),
        sa.Column('layup_mixmaster', sa.String(50), nullable=False, default="Hall of Fame"),
        sa.Column('lightning_launch', sa.String(50), nullable=False, default="Hall of Fame"),
        sa.Column('limitless_range', sa.String(50), nullable=False, default="Hall of Fame"),
        sa.Column('mini_marksman', sa.String(50), nullable=False, default="Hall of Fame"),
        sa.Column('off_ball_pest', sa.String(50), nullable=False, default="Hall of Fame"),
        sa.Column('on_ball_menace', sa.String(50), nullable=False, default="Hall of Fame"),
        sa.Column('paint_patroller', sa.String(50), nullable=False, default="Hall of Fame"),
        sa.Column('paint_prodigy', sa.String(50), nullable=False, default="Hall of Fame"),
        sa.Column('pick_dodger', sa.String(50), nullable=False, default="Hall of Fame"),
        sa.Column('pogo_stick', sa.String(50), nullable=False, default="Hall of Fame"),
        sa.Column('posterizer', sa.String(50), nullable=False, default="Hall of Fame"),
        sa.Column('post_fade_phenom', sa.String(50), nullable=False, default="Hall of Fame"),
        sa.Column('post_lockdown', sa.String(50), nullable=False, default="Hall of Fame"),
        sa.Column('post_powerhouse', sa.String(50), nullable=False, default="Hall of Fame"),
        sa.Column('post_up_poet', sa.String(50), nullable=False, default="Hall of Fame"),
        sa.Column('physical_finisher', sa.String(50), nullable=False, default="Hall of Fame"),
        sa.Column('rebound_chaser', sa.String(50), nullable=False, default="Hall of Fame"),
        sa.Column('set_shot_specialist', sa.String(50), nullable=False, default="Hall of Fame"),
        sa.Column('shifty_shooter', sa.String(50), nullable=False, default="Hall of Fame"),
        sa.Column('slippery_off_ball', sa.String(50), nullable=False, default="Hall of Fame"),
        sa.Column('strong_handle', sa.String(50), nullable=False, default="Hall of Fame"),
        sa.Column('unpluckable', sa.String(50), nullable=False, default="Hall of Fame"),
        sa.Column('versatile_visionary', sa.String(50), nullable=False, default="Hall of Fame")
    )


def downgrade():
    # Drop the player_targets table during downgrade
    op.drop_table('player_targets')
    