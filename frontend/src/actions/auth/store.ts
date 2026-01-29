export const useAuthStore = () => {
    return {
        logout: () => {
            console.log('Logging out...');
            // In a real app, this would clear tokens and redirect
        }
    }
}
