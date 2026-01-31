export const useAuthStore = () => {
    return {
        logout: async () => {
            console.log('Logging out...');
            if (typeof window !== 'undefined') {
                localStorage.removeItem('access_token');
                localStorage.removeItem('user_data');
            }
        }
    }
}
