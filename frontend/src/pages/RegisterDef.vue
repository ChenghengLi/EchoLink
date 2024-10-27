<template>
    <div class="home-two-light home-light container">

        <HeaderComponent />
        <!-- Set a fixed width for the container -->
        <div class="form-container mx-auto p-4 mt-8 border-3 rounded-lg border-indigo-100 bg-indigo-200">
            <div class="mb-3">
                <h2>Register</h2>
                <p>Already got an account? <RouterLink to="/login">Log-in instead.</RouterLink></p>
            </div>

            <!-- Form field container -->
            <div class="px-4 mx-auto">
                <!-- Basic info -->
                <TextInput label="Username" :required="true" placeholder="Username" input-type="text" :value="username" @changed="username = $event" :warning="usernameWarning" :test-id="'field-username'"></TextInput>
                <TextInput label="E-mail" :required="true" placeholder="example@example.com" input-type="email" :value="email" @changed="email = $event" :warning="emailWarning" :test-id="'field-email'"></TextInput>
                
                <hr class="h-divider"/>

                <!-- Password -->
                <TextInput label="Password" :required="true" placeholder="" input-type="password" :value="password" @changed="password = $event" :warning="passwordWarning" :test-id="'field-password'"></TextInput>
                <TextInput label="Confirm password" :required="true" placeholder="" input-type="password" :value="passwordConfirmation" @changed="passwordConfirmation = $event" :warning="passwordConfirmationWarning" :test-id="'field-passwordconfirmation'"></TextInput>
                
                <hr class="h-divider"/>

                <Checkbox label="I agree to the terms of service *" :checked="termsOfServiceChecked" @changed="termsOfServiceChecked = $event" :test-id="'checkbox-tos'"></Checkbox>
            </div>

            <button class="btn btn--primary w-100 w-md-60" :disabled="!canRegister" @click="register" :data-test="'button-register'">Register</button>
        </div>
        <FooterComponent class="footer-light mx-10" />
    </div>
</template>

<script setup>
import HeaderComponent from '../components/HeaderComponent.vue';
import FooterComponent from '../components/FooterComponent.vue';
import TextInput from '../components/form/TextInput.vue';
import Checkbox from '../components/form/CheckBox.vue';
import UserService from '../services/user.js'
import Swal from 'sweetalert2'
import Cookies from 'js-cookie'
import { computed, ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter()
const Toast = Swal.mixin({
  toast: true,
  position: 'top',
  iconColor: 'white',
  customClass: {
    popup: 'colored-toast',
  },
  showConfirmButton: false,
  timer: 1500,
  timerProgressBar: false,
})

const username = ref('')
const email = ref('')
const password = ref('')
const passwordConfirmation = ref('')
const termsOfServiceChecked = ref(false)

function register() {
    UserService.registerAccount(username.value, email.value, password.value).then(() => {
        Toast.fire({
            title: 'Registration successful!',
            icon: 'success',
        })
        router.push('/') // Go to homepage
        Cookies.set('logged_in', 'true', { expires: 7 }) // Expire login flag after 7 days
    }).catch((err) => {
        Swal.fire({
            title: 'Registration failed',
            text: 'Reason: ' + err.message,
            icon: 'error',
        })
    })
}

const isUsernameValid = computed(() => {
    // 4-16 characters, can include digits and underscore
    const regex = RegExp(/^([a-zA-Z0-9_]{4,16})$/)
    return regex.test(username.value)
})

const isEmailValid = computed(() => {
    // Pattern source: https://stackoverflow.com/a/46181
    const regex = RegExp(/^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/)
    return regex.test(email.value)
})

const isPasswordValid = computed(() => {
    return password.value.length >= 8 // 8+ characters
})

const passwordMatches = computed(() => {
    return password.value === passwordConfirmation.value
})

const canRegister = computed(() => {
    return isUsernameValid.value && isEmailValid.value && isPasswordValid.value && passwordMatches.value && termsOfServiceChecked.value
})

// Warnings for invalid fields
const usernameWarning = computed(() => {
    return (username.value !== '' && !isUsernameValid.value) ? 'Must be 4-16 letters, digits or underscores' : null
})
const emailWarning = computed(() => {
    return (email.value !== '' && !isEmailValid.value) ? 'Must be a valid address' : null
})
const passwordWarning = computed(() => {
    return (password.value !== '' && !isPasswordValid.value) ? 'Must be 8+ characters' : null
})
const passwordConfirmationWarning = computed(() => {
    return (passwordConfirmation.value !== '' && !passwordMatches.value) ? 'Passwords must match' : null
})

</script>


<style scoped>
.form-container {
    width: 100%; /* Full width by default */
    width: 600px;
    box-sizing: border-box; /* Include padding and border in the element's total width and height */
}
.container{
    width: 100vw;
}

@media (max-width: 768px) {
    .form-container {
        width: 100vw; /* Full viewport width for small screens */
        height: 100vh; /* Full viewport height for small screens */
        margin: 0; /* Remove margin for full screen effect */
        border-radius: 0; /* Remove border radius for full screen effect */
    }
}
</style>