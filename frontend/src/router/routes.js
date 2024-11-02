

import HomeDef from '../pages/HomeDef.vue'
import RegisterDef from '../pages/RegisterDef.vue'
import ProfileDef from '../pages/ProfileDef.vue'

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
            path: '/users/:username',
            name: 'User Profile',
            component: ProfileDef,
        }
    ];
