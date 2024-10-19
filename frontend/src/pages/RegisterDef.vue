<template>
	<div class="home-two-light home-light">
        <Header/>
        <!-- Extra margin at top for spacing between header -->
		<div class="mx-auto max-w-lg p-4 mt-8 border-3 rounded-lg border-indigo-100 bg-indigo-200">
            <div class="mb-3">
                <h2>Register</h2>
                <p>Already got an account? <RouterLink to="/login">Log-in instead.</RouterLink></p>
            </div>

            <!-- Form field container -->
            <div class="px-4 mx-auto">
                <!-- Basic info -->
                <TextInput label="Username" placeholder="Username" input-type="text" :value="username" @changed="username = $event"></TextInput>
                <TextInput label="E-mail" placeholder="example@example.com" input-type="email" :value="email" @changed="email = $event"></TextInput>
                
                <hr class="h-divider"/>

                <!-- Password -->
                <TextInput label="Password" placeholder="" input-type="password" :value="password" @changed="password = $event"></TextInput>
                <TextInput label="Confirm password" placeholder="" input-type="password" :value="passwordConfirmation" @changed="passwordConfirmation = $event"></TextInput>
                
                <hr class="h-divider"/>

                <Checkbox label="I agree to the terms of service" :checked="termsOfServiceChecked" @changed="termsOfServiceChecked = $event" ></Checkbox>
            </div>

            <button class="btn btn--primary w-60" :disabled="!canRegister">Register</button>
		</div>
        <Footer class="footer-light mx-10" />
	</div>
</template>

<script setup>
import Header from '../components/Header.vue'
import Footer from '../components/Footer.vue'
import TextInput from '../components/form/TextInput.vue';
import Checkbox from '../components/form/Checkbox.vue';
import { computed, ref } from 'vue';

const username = ref('')
const email = ref('')
const password = ref('')
const passwordConfirmation = ref('')
const termsOfServiceChecked = ref(false)

const isUsernameValid = computed(() => {
    // 4-16 characters, can include digits and underscore
    let regex = RegExp(/^([a-zA-Z0-9_]{4,16})$/)
    return regex.test(username.value)
})

const isEmailValid = computed(() => {
    // Pattern source: https://stackoverflow.com/a/46181
    let regex = RegExp(/^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/)
    return regex.test(email.value)
})

const isPasswordValid = computed(() => {
    return password.value.length >= 8 // 8+ characters
})

const passwordMatches = computed(() => {
    return password.value == passwordConfirmation.value
})

const canRegister = computed(() => {
    return isUsernameValid.value && isEmailValid.value && isPasswordValid.value && passwordMatches.value && termsOfServiceChecked.value
})

</script>
