// starts pythons download function with url parameter
function indirmeye_basla(){
  let url = document.getElementById('url-field').value;
  //console.log("downloading video: " + url);
  eel.indir(url);
}

// opens directory selection window
async function dizin_tarayicisi_ac() {
  var download_path = await eel.dizin_tarayicisi_ac()();
}

// get video_id from url (thanks https://stackoverflow.com/questions/3452546/how-do-i-get-the-youtube-video-id-from-a-url)
function youtube_url_ayikla(url){
    var regExp  = /^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*/;
    var match   = url.match(regExp);
    return (match&&match[7].length==11)? match[7] : false;
}

// changes thumbnail (runs every second (not the best solution i know))
function kucuk_resim_guncelle() {
  let url         = document.getElementById('url-field').value;
  let video_id    = youtube_url_ayikla(url);
  let picture_url = 'img/noinput.svg';
  if(video_id !== false) {
    picture_url = 'https://img.youtube.com/vi/' + video_id + '/0.jpg';
  }
  document.getElementById('video-thumbnail').src = picture_url;
}

// update progress bar via python backend
eel.expose(guncelle_progress);
function guncelle_progress(percentage) {
  let pb = document.getElementById('progress_bar0');
  pb.style.width = percentage.toString() + "%";
  pb.innerHTML = percentage.toString() + "%";
}

// reset progress bar
function sifirla_progress() {
  let pb = document.getElementById('progress_bar0');
  pb.style.width = "0%"
  pb.innerHTML = "";
}

// update status field
eel.expose(guncelle_durum);
function guncelle_durum(msg) {
  document.getElementById('status-field').value = "[Durum] " + msg;
}

// update version text of the version badge
eel.expose(guncelle_version_rozeti)
function guncelle_version_rozeti(version) {
  document.getElementById('version-badge').innerHTML = version;
}

// shows the update available badge
eel.expose(mevcut_guncellemeyi_goster)
function mevcut_guncellemeyi_goster() {
  document.getElementById('update-available').style="visibility: visible";
}
