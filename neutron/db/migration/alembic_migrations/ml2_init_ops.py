# Copyright 2014 OpenStack Foundation
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

# Initial operations for ML2 plugin and drivers


from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'ml2_vlan_allocations',
        sa.Column('physical_network', sa.String(length=64), nullable=False),
        sa.Column('vlan_id', sa.Integer(), autoincrement=False,
                  nullable=False),
        sa.Column('allocated', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('physical_network', 'vlan_id'),
        sa.Index(op.f('ix_ml2_vlan_allocations_physical_network_allocated'),
                 'physical_network', 'allocated'))

    op.create_table(
        'ml2_vxlan_endpoints',
        sa.Column('ip_address', sa.String(length=64), nullable=False),
        sa.Column('udp_port', sa.Integer(), autoincrement=False,
                  nullable=False),
        sa.Column('host', sa.String(length=255), nullable=True),
        sa.UniqueConstraint('host', name='unique_ml2_vxlan_endpoints0host'),
        sa.PrimaryKeyConstraint('ip_address'))

    op.create_table(
        'ml2_gre_endpoints',
        sa.Column('ip_address', sa.String(length=64), nullable=False),
        sa.Column('host', sa.String(length=255), nullable=True),
        sa.UniqueConstraint('host', name='unique_ml2_gre_endpoints0host'),
        sa.PrimaryKeyConstraint('ip_address'))

    op.create_table(
        'ml2_geneve_endpoints',
        sa.Column('ip_address', sa.String(length=64), nullable=False),
        sa.Column('host', sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint('ip_address'),
        sa.UniqueConstraint('host', name='unique_ml2_geneve_endpoints0host'),
    )

    op.create_table(
        'ml2_vxlan_allocations',
        sa.Column('vxlan_vni', sa.Integer(), autoincrement=False,
                  nullable=False),
        sa.Column('allocated', sa.Boolean(), nullable=False,
                  server_default=sa.sql.false(), index=True),
        sa.PrimaryKeyConstraint('vxlan_vni'))

    op.create_table(
        'ml2_gre_allocations',
        sa.Column('gre_id', sa.Integer(), autoincrement=False,
                  nullable=False),
        sa.Column('allocated', sa.Boolean(), nullable=False,
                  server_default=sa.sql.false(), index=True),
        sa.PrimaryKeyConstraint('gre_id'))

    op.create_table(
        'ml2_geneve_allocations',
        sa.Column('geneve_vni', sa.Integer(),
                  autoincrement=False, nullable=False),
        sa.Column('allocated', sa.Boolean(), nullable=False,
                  server_default=sa.sql.false(), index=True),
        sa.PrimaryKeyConstraint('geneve_vni'),
    )

    op.create_table(
        'ml2_flat_allocations',
        sa.Column('physical_network', sa.String(length=64), nullable=False),
        sa.PrimaryKeyConstraint('physical_network'))

    op.create_table(
        'ml2_network_segments',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('network_id', sa.String(length=36), nullable=False),
        sa.Column('network_type', sa.String(length=32), nullable=False),
        sa.Column('physical_network', sa.String(length=64), nullable=True),
        sa.Column('segmentation_id', sa.Integer(), nullable=True),
        sa.Column('is_dynamic', sa.Boolean(), nullable=False,
                  server_default=sa.sql.false()),
        sa.Column('segment_index', sa.Integer(), nullable=False,
                  server_default='0'),
        sa.ForeignKeyConstraint(['network_id'], ['networks.id'],
                                ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'))

    op.create_table(
        'ml2_port_bindings',
        sa.Column('port_id', sa.String(length=36), nullable=False),
        sa.Column('host', sa.String(length=255), nullable=False,
                  server_default=''),
        sa.Column('vif_type', sa.String(length=64), nullable=False),
        sa.Column('vnic_type', sa.String(length=64), nullable=False,
                  server_default='normal'),
        sa.Column('profile', sa.String(length=4095), nullable=False,
                  server_default=''),
        sa.Column('vif_details', sa.String(length=4095), nullable=False,
                  server_default=''),
        sa.ForeignKeyConstraint(['port_id'], ['ports.id'],
                                ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('port_id'))

    op.create_table(
        'ml2_port_binding_levels',
        sa.Column('port_id', sa.String(length=36), nullable=False),
        sa.Column('host', sa.String(length=255), nullable=False),
        sa.Column('level', sa.Integer(), autoincrement=False, nullable=False),
        sa.Column('driver', sa.String(length=64), nullable=True),
        sa.Column('segment_id', sa.String(length=36), nullable=True),
        sa.ForeignKeyConstraint(['port_id'], ['ports.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['segment_id'], ['ml2_network_segments.id'],
                                ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('port_id', 'host', 'level')
    )

    op.create_table(
        'cisco_ml2_nexusport_bindings',
        sa.Column('binding_id', sa.Integer(), nullable=False),
        sa.Column('port_id', sa.String(length=255), nullable=True),
        sa.Column('vlan_id', sa.Integer(), autoincrement=False,
                  nullable=False),
        sa.Column('switch_ip', sa.String(length=255), nullable=True),
        sa.Column('instance_id', sa.String(length=255), nullable=True),
        sa.Column('vni', sa.Integer(), nullable=True),
        sa.Column('is_provider_vlan', sa.Boolean(), nullable=False,
                  server_default=sa.sql.false()),
        sa.PrimaryKeyConstraint('binding_id'),
    )

    op.create_table(
        'arista_provisioned_nets',
        sa.Column('tenant_id', sa.String(length=255), nullable=True,
                  index=True),
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('network_id', sa.String(length=36), nullable=True),
        sa.Column('segmentation_id', sa.Integer(),
                  autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint('id'))

    op.create_table(
        'arista_provisioned_vms',
        sa.Column('tenant_id', sa.String(length=255), nullable=True,
                  index=True),
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('vm_id', sa.String(length=255), nullable=True),
        sa.Column('host_id', sa.String(length=255), nullable=True),
        sa.Column('port_id', sa.String(length=36), nullable=True),
        sa.Column('network_id', sa.String(length=36), nullable=True),
        sa.PrimaryKeyConstraint('id'))

    op.create_table(
        'arista_provisioned_tenants',
        sa.Column('tenant_id', sa.String(length=255), nullable=True,
                  index=True),
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.PrimaryKeyConstraint('id'))

    op.create_table(
        'ml2_nexus_vxlan_allocations',
        sa.Column('vxlan_vni', sa.Integer(), nullable=False,
                  autoincrement=False),
        sa.Column('allocated', sa.Boolean(), nullable=False,
                  server_default=sa.sql.false()),
        sa.PrimaryKeyConstraint('vxlan_vni')
    )

    op.create_table(
        'ml2_nexus_vxlan_mcast_groups',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('mcast_group', sa.String(length=64), nullable=False),
        sa.Column('associated_vni', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['associated_vni'],
                                ['ml2_nexus_vxlan_allocations.vxlan_vni'],
                                ondelete='CASCADE')
    )

    op.create_table(
        'cisco_ml2_nexus_nve',
        sa.Column('vni', sa.Integer(), nullable=False),
        sa.Column('switch_ip', sa.String(length=255), nullable=True),
        sa.Column('device_id', sa.String(length=255), nullable=True),
        sa.Column('mcast_group', sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint('vni', 'switch_ip', 'device_id'))
