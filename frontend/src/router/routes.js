

import HomeDef from '../pages/HomeDef.vue'
import RegisterDef from '../pages/RegisterDef.vue'
import ProfileDef from '../pages/ProfileDef.vue'
import LogInDef from '../pages/LogInDef.vue';
import PlaylistCreator from '../pages/PlaylistCreator.vue';
import UploadTrack from '../pages/UploadTrack.vue';

export default  [
        {
            path: '/',
            name: 'Home',
            component: HomeDef,
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
            path: '/uploadTrack',
            name: 'Upload Track',
            component: UploadTrack,
            beforeEnter: (to, from, next) => {
                const isArtist = UserService.getUserRole() === 'artist'; // Verifica si el usuario es un artista
                if (isArtist) {
                  next(); // Si es artista, deja pasar a la ruta
                } else {
                  next('/'); // Si no es artista, redirige a la home u otra página
                }
              },
        },
    ];
