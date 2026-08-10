<template>
  <div>
    <p>Redirecting to home...</p>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'

const error = useError()

onMounted(() => {
  if (error.value && error.value.statusCode === 404) {
    clearError({ redirect: '/champdle/' })
  } else {
    clearError({ redirect: '/champdle/' })
  }
})
</script>
