'use client';

import { useState, useEffect } from 'react';
import { Search, Plus, UserPlus } from 'lucide-react';
import TableArchive, { Column } from '@/components/common/TableArchive';
import { authActions } from '@/actions/auth/auth.actions';
import { User, RegisterData } from '@/types/auth';
import { Role } from '@/types/user';

export default function AdminUsers() {
    const [users, setUsers] = useState<User[]>([]);
    const [roles, setRoles] = useState<Role[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');
    const [showAddModal, setShowAddModal] = useState(false);
    const [newUser, setNewUser] = useState<RegisterData>({
        username: '',
        email: '',
        password: '',
        first_name: '',
        last_name: '',
    });

    const fetchUsers = async () => {
        try {
            setIsLoading(true);
            const data = await authActions.listUsers();
            setUsers(data);
        } catch (error) {
            console.error('Error fetching users:', error);
        } finally {
            setIsLoading(false);
        }
    };

    const fetchRoles = async () => {
        try {
            const data = await authActions.getAllRoles();
            setRoles(data);
        } catch (error) {
            console.error('Error fetching roles:', error);
        }
    };

    useEffect(() => {
        fetchUsers();
        fetchRoles();
    }, []);

    const handleAddUser = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            await authActions.register(newUser);
            setShowAddModal(false);
            setNewUser({
                username: '',
                email: '',
                password: '',
                first_name: '',
                last_name: '',
            });
            fetchUsers();
        } catch (error: any) {
            alert(error.message || 'Failed to add user');
        }
    };

    const handleRoleChange = async (userId: number, roleId: number) => {
        try {
            await authActions.assignRole(userId, roleId, 1); // assigned_by will be replaced by API from token
            fetchUsers();
            alert('Role updated successfully');
        } catch (error: any) {
            alert(error.message || 'Failed to update role');
        }
    };

    const columns: Column<User>[] = [
        {
            key: 'username',
            title: 'Username',
            sortable: true,
            render: (value) => <span className="text-sm font-medium text-gray-900">{value}</span>,
        },
        {
            key: 'email',
            title: 'Email',
            sortable: true,
            render: (value) => <span className="text-sm text-gray-500">{value}</span>,
        },
        {
            key: 'first_name',
            title: 'Full Name',
            sortable: true,
            render: (value, row) => (
                <span className="text-sm text-gray-900">
                    {row.first_name} {row.last_name || ''}
                </span>
            ),
        },
        {
            key: 'primary_role_id',
            title: 'Role',
            sortable: true,
            render: (value, row) => (
                <select
                    className="text-xs border border-gray-300 rounded-md px-2 py-1 bg-white focus:outline-none focus:ring-1 focus:ring-primary-500"
                    value={value || ''}
                    onChange={(e) => handleRoleChange(row.id, parseInt(e.target.value))}
                >
                    <option value="">Select Role</option>
                    {roles.map((role) => (
                        <option key={role.id} value={role.id}>
                            {role.name}
                        </option>
                    ))}
                </select>
            ),
        },
        {
            key: 'active_or_archive',
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
    ];

    const filteredUsers = users.filter(
        (user) =>
            user.username.toLowerCase().includes(searchTerm.toLowerCase()) ||
            user.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
            user.first_name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div className="p-6">
            <div className="flex justify-between items-center mb-6">
                <div>
                    <h1 className="text-3xl font-bold text-gray-800">User Management</h1>
                    <p className="text-gray-600 mt-1">Manage system users and their access</p>
                </div>
                <button
                    onClick={() => setShowAddModal(true)}
                    className="flex items-center gap-2 bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors"
                >
                    <UserPlus className="w-5 h-5" />
                    Add User
                </button>
            </div>

            <div className="bg-white rounded-lg shadow-md p-4 mb-6">
                <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                    <input
                        type="text"
                        placeholder="Search users by name, email or username..."
                        className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                </div>
            </div>

            <div className="bg-white rounded-lg shadow-md overflow-hidden">
                {isLoading ? (
                    <div className="p-10 text-center text-gray-500">Loading users...</div>
                ) : (
                    <TableArchive
                        data={filteredUsers}
                        columns={columns}
                        itemsPerPage={10}
                        emptyMessage="No users found"
                    />
                )}
            </div>

            {/* Add User Modal */}
            {showAddModal && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
                    <div className="bg-white rounded-xl shadow-2xl w-full max-w-md p-6">
                        <h2 className="text-xl font-bold mb-4">Add New User</h2>
                        <form onSubmit={handleAddUser} className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Username</label>
                                <input
                                    type="text"
                                    required
                                    className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                                    value={newUser.username}
                                    onChange={(e) => setNewUser({ ...newUser, username: e.target.value })}
                                />
                            </div>
                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">First Name</label>
                                    <input
                                        type="text"
                                        required
                                        className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                                        value={newUser.first_name}
                                        onChange={(e) => setNewUser({ ...newUser, first_name: e.target.value })}
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">Last Name</label>
                                    <input
                                        type="text"
                                        className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                                        value={newUser.last_name}
                                        onChange={(e) => setNewUser({ ...newUser, last_name: e.target.value })}
                                    />
                                </div>
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                                <input
                                    type="email"
                                    required
                                    className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                                    value={newUser.email}
                                    onChange={(e) => setNewUser({ ...newUser, email: e.target.value })}
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
                                <input
                                    type="password"
                                    required
                                    minLength={8}
                                    className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                                    value={newUser.password}
                                    onChange={(e) => setNewUser({ ...newUser, password: e.target.value })}
                                />
                            </div>
                            <div className="flex justify-end gap-3 mt-6">
                                <button
                                    type="button"
                                    onClick={() => setShowAddModal(false)}
                                    className="px-4 py-2 text-gray-600 hover:text-gray-800"
                                >
                                    Cancel
                                </button>
                                <button
                                    type="submit"
                                    className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700"
                                >
                                    Create User
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
}
