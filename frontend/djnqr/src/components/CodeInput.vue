<template>
  <v-card class="pa-4 d-flex flex-column align-center text-center" max-width="500" min-height="250" outlined>
    <v-card-title class="text-h6">Enter Code</v-card-title>

    <v-card-text class="w-100 d-flex flex-column" style="gap: 1.5rem;">
      <v-text-field v-model="code" label="Code" @keydown.enter="submit" outlined hide-details class="mx-auto"
        style="width: 100%;" />

      <v-btn color="primary" @click="submit" size="large" class="mx-auto px-6">
        Submit
      </v-btn>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { ref, defineEmits } from 'vue';

const code = ref('');
const emit = defineEmits(['submit']);

const submit = () => {
  if (!code.value) return;
  emit('submit', code.value);
};
</script>
