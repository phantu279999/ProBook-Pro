const downloadButton = document.getElementById('downloadButton');

downloadButton.addEventListener('click', () => {
  // Replace 'your_file.pdf' with the actual file path
  const filePath = '/media/store_data/video_youtube.csv';

  // Create a link element
  const link = document.createElement('a');
  link.href = filePath;
  link.download = 'video_youtube.csv'; // Set the desired download filename

  // Trigger the download
  link.click();
});