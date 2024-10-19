<template>
	<div class="mb-3">
        <div class="flex flex-row justify-between">
            <label for="inputField" class="block text-sm font-medium text-left ml-1 mb-2">{{ label }} {{ required && " *" }}</label>
            <p v-if="warning" class="text-sm text-red-500 font-medium">{{ warning }}</p>
        </div>
        <input :type="inputType" id="inputField" class="p-2.5 bg-gray-50 border border-gray-300 text-sm rounded-lg block w-full" :placeholder="placeholder" :pattern="pattern" @change="$emit('changed', $event.target.value)" @keyup="$emit('changed', $event.target.value)" required /> <!-- Emit event also on key release (usually it's only on submit) -->
  </div>
</template>

<script setup>
defineProps({
    "label": String,
    "placeholder": String,
    "inputType": String, // HTML <input> form type
    "pattern": String, // Form pattern to enforce
    "warning": String, // Shows an extra red label on the right
    "required": Boolean, // Shows a * by the label
})
</script>

<style scoped>
input {
  @apply focus:ring-blue-50 bg-gray-700 border-gray-600 placeholder-gray-400 text-white focus:border-blue-500
}
</style>
