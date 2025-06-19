import { io } from "https://cdn.socket.io/4.7.5/socket.io.esm.min.js";

export function startCamera(op = 'markin', fps = 5) {
  const socket = io();
  const video = document.querySelector('#video');
  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d');

  navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
    video.srcObject = stream;
    video.play();
    const interval = setInterval(() => {
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
      const dataURL = canvas.toDataURL('image/jpeg', 0.7);
      socket.emit('video_frame', { image: dataURL, op });
    }, 1000 / fps);

    socket.on('match_result', payload => {
      if (payload.op !== op) return;
      console.log('Server says:', payload.result);
    });
  }).catch(err => alert('Camera error: ' + err));
}
