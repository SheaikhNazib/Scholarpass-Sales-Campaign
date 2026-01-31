'use client';

import { useState, useEffect } from 'react';
import { ShieldCheck, Plus, Search } from 'lucide-react';
import TableArchive, { Column } from '@/components/common/TableArchive';
import { authActions } from '@/actions/auth/auth.actions';
import { Role } from '@/types/user';

export default function AdminRoles() {
    const [roles, setRoles] = useState<Role[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');

    const fetchRoles = async () => {
        try {
            setIsLoading(true);
            const data = await authActions.getAllRoles();
            setRoles(data);
        } catch (error) {
            console.error('Error fetching roles:', error);
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        fetchRoles();
    }, []);

    const columns: Column<Role>[] = [
        {
            key: 'name',
            title: 'Role Name',
            sortable: true,
            render: (value) => <span className="text-sm font-medium text-gray-900">{value}</span>,
        },
        {
            key: 'description',
            title: 'Description',
            sortable: false,
            render: (value) => <span className="text-sm text-gray-500">{value || 'No description'}</span>,
        },
        {
            key: 'is_active',
            title: 'Status',
            sortable: true,
            render: (value) => (
                <span
                    className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${value ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                        }`}
                >
                    {value ? 'Active' : 'Inactive'}
                </span>
            ),
        },
        {
            key: 'display_sequence',
            title: 'Order',
            sortable: true,
            render: (value) => <span className="text-sm text-gray-500">{value}</span>,
        },
    ];

    const filteredRoles = roles.filter(
        (role) =>
            role.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            (role.description && role.description.toLowerCase().includes(searchTerm.toLowerCase()))
    );

    return (
        <div className="p-6">
            <div className="flex justify-between items-center mb-6">
                <div>
                    <h1 className="text-3xl font-bold text-gray-800">Role Management</h1>
                    <p className="text-gray-600 mt-1">Define and manage company roles</p>
                </div>
                <button
                    className="flex items-center gap-2 bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors opacity-50 cursor-not-allowed"
                    title="Role creation coming soon"
                    disabled
                >
                    <Plus className="w-5 h-5" />
                    Add Role
                </button>
            </div>

            <div className="bg-white rounded-lg shadow-md p-4 mb-6">
                <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                    <input
                        type="text"
                        placeholder="Search roles..."
                        className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                </div>
            </div>

            <div className="bg-white rounded-lg shadow-md overflow-hidden">
                {isLoading ? (
                    <div className="p-10 text-center text-gray-500">Loading roles...</div>
                ) : (
                    <TableArchive
                        data={filteredRoles}
                        columns={columns}
                        itemsPerPage={10}
                        emptyMessage="No roles found"
                    />
                )}
            </div>
        </div>
    );
}
