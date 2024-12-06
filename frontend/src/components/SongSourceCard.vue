<!-- A searchable dropdown form component. -->
<template>
	<a :href="props.link" class="flex flex-col lg:w-52 w-36 p-3 rounded-2xl h-fit hover:shadow-lg hover:cursor-pointer">
        <img :src="props.img" class="mx-auto lg:size-24 size-16"/>
        <a :href="props.link" class="mx-auto text-sm text-nowrap">{{ props.label }}</a>
    </a>
</template>

<script setup>

const props = defineProps({
    "label": String,
    "img": String, // Image path
    "link": String,
})

</script>

<style scoped>

</style>
