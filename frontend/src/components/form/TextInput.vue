<template>
	<div class="mb-3">
        <label for="inputField" class="block text-sm font-medium text-left ml-1 mb-2">{{ label }}</label>
        <input :type="inputType" id="inputField" class="p-2.5 bg-gray-50 border border-gray-300 text-sm rounded-lg block w-full" :placeholder="placeholder" :pattern="pattern" required />
  </div>
</template>

<script setup>
defineProps({
    "label": String,
    "placeholder": String,
    "inputType": String,
    "required": Boolean,
    "pattern": String,
})
</script>

<style scoped>
input {
  @apply focus:ring-blue-50 bg-gray-700 border-gray-600 placeholder-gray-400 text-white focus:border-blue-500
}
</style>
