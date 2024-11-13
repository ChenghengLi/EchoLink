

import HomeDef from '../pages/HomeDef.vue'
import RegisterDef from '../pages/RegisterDef.vue'
import ProfileDef from '../pages/ProfileDef.vue'
import LogInDef from '../pages/LogInDef.vue';

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
    ];
