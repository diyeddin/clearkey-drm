const manifestUri = 'rick/rick_master.m3u8';
const licenseServerUrl = 'http://localhost:8080/license'

async function init() {
  const video = document.getElementById('video');
  const ui = video['ui'];
  const controls = ui.getControls();
  const player = controls.getPlayer();

  window.player = player;
  window.ui = ui;

  player.addEventListener('error', onPlayerErrorEvent);
  controls.addEventListener('error', onUIErrorEvent);

  player.configure({
    drm: {
      servers: {
        'org.w3.clearkey': licenseServerUrl
      }
    }
  });

  try {
    await player.load(manifestUri);
    console.log('The video has now been loaded!');
  } catch (error) {
    onPlayerError(error);
    }
}

function onPlayerErrorEvent(errorEvent) {
  onPlayerError(event.detail);
}
function onPlayerError(error) {
  console.error('Error code', error.code, 'object', error);
}
function onUIErrorEvent(errorEvent) {
  onPlayerError(event.detail);
}
function initFailed(errorEvent) {
  console.error('Unable to load the UI library!');
}
document.addEventListener('shaka-ui-loaded', init);
document.addEventListener('shaka-ui-load-failed', initFailed);
