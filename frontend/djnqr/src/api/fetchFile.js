export async function fetchFileById(id) {
  const apiUrl = `http://localhost:8000/data/${id}`;

  try {
    console.log(`Fetching file for ID: ${id}`); // Log the ID you're fetching
    const response = await fetch(apiUrl);

    console.log('Response Status:', response.status); // Log response status
    console.log('Response OK:', response.ok); // Log if the response is OK

    if (!response.ok) {
      throw new Error('File not found');
    }

    const blob = await response.blob();
    console.log('Blob:', blob); // Log the blob to inspect the file content

    const fileUrl = URL.createObjectURL(blob);
    window.open(fileUrl, '_blank');
  } catch (error) {
    console.error('Error fetching file:', error);
    alert('Error details: ' + error.message); // Show error message in alert for debugging
    throw error; // Rethrow the error to be caught by the outer try-catch block
  }
}

