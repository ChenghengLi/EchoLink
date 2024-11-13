import { mount } from '@vue/test-utils'
import { describe, it, expect } from 'vitest'
import HeaderComponent from '../components/HeaderComponent.vue'
import Cookies from 'js-cookie'
import { createRouter, createWebHistory } from 'vue-router'

const routes = [{ path: '/', component: { template: '<div>Home</div>' } }]
const router = createRouter({
    history: createWebHistory(),
    routes,
})

describe('Header Component - Log Out Tests', () => {
    beforeAll(async () => {
        router.push('/')
        await router.isReady()
    })

    it('should render Log Out button when logged in', async () => {
        Cookies.set('logged_in', 'true') // Simulate logged-in state
        const wrapper = mount(HeaderComponent, {
            global: {
                plugins: [router],
            },
            props: { LogoSrc: 'path/to/logo.png' }
        })
        
        expect(wrapper.find('[data-test="button-logout"]').exists()).toBe(true) // Log Out button should be present
    })

    it('should not render Log Out button when logged out', async () => {
        Cookies.remove('logged_in') // Simulate logged-out state
        const wrapper = mount(HeaderComponent, {
            global: {
                plugins: [router],
            },
            props: { LogoSrc: 'path/to/logo.png' }
        })

        expect(wrapper.find('[data-test="button-logout"]').exists()).toBe(false) // Log Out button should not be present
    })

    it('should change isLoggedIn state and redirect on Log Out', async () => {
        Cookies.set('logged_in', 'true')
        const wrapper = mount(HeaderComponent, {
            global: {
                plugins: [router],
            },
            props: { LogoSrc: 'path/to/logo.png' }
        })
        
        // Trigger logout
        await wrapper.get('[data-test="button-logout"]').trigger('click')
        
        expect(Cookies.get('logged_in')).toBeUndefined() // Check cookie removal
        expect(wrapper.vm.isLoggedIn).toBe(false) // Check isLoggedIn state
        expect(wrapper.vm.$route.path).toBe('/') // Check redirection to homepage
    })
})
