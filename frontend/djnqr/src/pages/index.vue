<template>
  <v-container class="fill-height" fluid>
    <v-row justify="center" align="center">
      <v-col cols="12" sm="10" md="6" lg="4">
        <!-- Title -->
        <v-card class="pa-4 mb-6" outlined>
          <v-card-title class="text-h3 text-center">DJN QR</v-card-title>
        </v-card>

        <!-- Tab Navigation -->
        <v-tabs v-model="tab" background-color="primary" dark>
          <v-tab value="get">Download</v-tab>
          <v-tab value="upload">Upload</v-tab>
        </v-tabs>

        <!-- Tab Content -->
        <v-window v-model="tab" class="mt-4">

          <v-window-item value="get">
            <CodeInput @submit="handleSubmit" />
          </v-window-item>

          <v-window-item value="upload">
            <FileUpload />
          </v-window-item>
        </v-window>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue';
import FileUpload from '@/components/FileUpload.vue';
import CodeInput from '@/components/CodeInput.vue';

import { fetchFileById } from '@/api/fetchFile';

const tab = ref('get');

const handleSubmit = async (code) => {
  try {
    await fetchFileById(code);
    alert(`File fetched for code: ${code}`);
  } catch (err) {
    alert('Could not fetch file. Please check the code and try again.');
  }
};
</script>
