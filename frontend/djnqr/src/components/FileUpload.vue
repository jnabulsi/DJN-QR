<template>
  <v-card class="pa-4 d-flex flex-column align-center text-center" max-width="500" min-height="250" outlined>
    <v-card-title class="text-h6">Upload File</v-card-title>

    <v-card-text class="w-100 d-flex flex-column" style="gap: 1.5rem;">
      <v-file-input v-model="file" label="Select file" accept="" prepend-icon="mdi-file-upload" outlined show-size
        class="mx-auto" style="width: 100%;" />

      <v-btn :disabled="!file" color="primary" @click="handleUpload" size="large" class="mx-auto px-6">
        Upload
      </v-btn>

      <v-alert v-if="message" :type="messageType" dense text class="mt-2">
        {{ message }}
      </v-alert>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { ref } from 'vue';
import { uploadFile } from '@/api/uploadFile';

const file = ref(null);
const message = ref('');
const messageType = ref('success');

const handleUpload = async () => {
  if (!file.value) return;

  try {
    const { id, qr_url } = await uploadFile(file.value);
    window.open(qr_url, '_blank');
    messageType.value = 'success';
    message.value = `Upload successful. ID: ${id}`;
    file.value = null;
  } catch (err) {
    console.error(err);
    messageType.value = 'error';
    message.value = 'Upload failed. Please try again.';
  }
};
</script>
