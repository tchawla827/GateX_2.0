const video = document.getElementById('cam');

if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
  navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
    video.srcObject = stream;
    video.play();

    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');

    setInterval(() => {
      if (video.videoWidth === 0) return;
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
      canvas.toBlob(blob => {
        if (blob) {
          fetch('/api/frame', {
            method: 'POST',
            headers: { 'Content-Type': 'image/jpeg' },
            body: blob
          })
            .then(res => res.json())
            .then(data => {
              console.log('Recognition result:', data);
            })
            .catch(err => console.error('Send frame error', err));
        }
      }, 'image/jpeg');
    }, 200);
  }).catch(err => {
    console.error('getUserMedia error:', err);
  });
} else {
  console.error('getUserMedia not supported');
}
