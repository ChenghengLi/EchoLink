

import HomeDef from '../pages/HomeDef.vue'
import RegisterDef from '../pages/RegisterDef.vue'
import ProfileDef from '../pages/ProfileDef.vue'
import LogInDef from '../pages/LogInDef.vue';
import PlaylistCreator from '../pages/PlaylistCreator.vue';
import UploadTrack from '../pages/UploadTrack.vue';
import UserService from '../services/user.js';
import ListenerDashboard from '../pages/ListenerDashboard.vue';
import ArtistDashboard from '../pages/ArtistDashboard.vue';

export default  [
        {
            path: '/',
            name: 'Home',
            component: async function() {
                return UserService.isLoggedIn() ? ListenerDashboard : HomeDef // Redirect to dashboard if logged-in
            },
        },
        {
            path: '/register',
            name: 'Resgister',
            component: RegisterDef,
        },
        {
            path: '/login',
            name: 'LogIn',
            component: LogInDef,
        },
        {
            path: '/users/:username',
            name: 'User Profile',
            component: ProfileDef,
        },
        {
            path: '/playlists/:id',
            name: 'Playlist',
            component: PlaylistCreator,
        },
        {
            path: '/dashboard/',
            name: 'Artist Dashboard',
            component: ArtistDashboard,
        },
        {
            path: '/uploadTrack',
            name: 'UploadTrack',
            component: UploadTrack,
            beforeEnter: async (to, from, next) => {
                try {
                    const username = UserService.getCurrentUsername();
                    if (!username) {
                        // Redirect to login page if no user is authenticated
                        next('/login');
                        return;
                    }
        
                    const role = await UserService.getUserRole(username); 
                    if (role === 'artist') {
                        next(); 
                    } else {
                        next('/'); // Redirect to the homepage if the user is not an artist
                    }
                } catch (error) {
                    console.error('Error comprobando el rol del usuario:', error);
                    next('/'); // Redirect to the homepage in case of an error
                }
            },
        },
    ];
