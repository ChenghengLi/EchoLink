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
                <TextInput label="Username" placeholder="Username" input-type="text"></TextInput>
                <TextInput label="E-mail" placeholder="example@example.com" input-type="email"></TextInput>
                
                <hr class="h-divider"/>

                <!-- Password -->
                <TextInput label="Password" placeholder="" input-type="password"></TextInput>
                <TextInput label="Confirm password" placeholder="" input-type="password"></TextInput>
                
                <hr class="h-divider"/>

                <Checkbox label="I agree to the terms of service"></Checkbox>
            </div>

            <button class="btn btn--primary w-60">Register</button>
		</div>
        <Footer class="footer-light mx-10" />
	</div>
</template>

<script setup>
import Header from '../components/Header.vue'
import Footer from '../components/Footer.vue'
import TextInput from '../components/form/TextInput.vue';
import Checkbox from '../components/form/Checkbox.vue';

</script>
