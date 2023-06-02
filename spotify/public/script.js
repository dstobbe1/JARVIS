async function getToken() {
  const response = await fetch("/getToken");
  const data = await response.text();
  return data;
}

async function getQueue() {
  const queueRes = await fetch("https://api.spotify.com/v1/me/player/queue", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return JSON.parse(await queueRes.text());
}

let token = getToken();

window.onSpotifyWebPlaybackSDKReady = async () => {
  token = await token;
  const player = new Spotify.Player({
    name: "Web Playback SDK Quick Start Player",
    getOAuthToken: (cb) => {
      cb(token);
    },
    volume: 0.5,
  });

  // Ready
  player.addListener("ready", ({ device_id }) => {
    console.log("Ready with Device ID", device_id);
    fetch("https://api.spotify.com/v1/me/player", {
      method: "PUT",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        device_ids: [device_id],
      }),
    }).then(() => console.log("transfered playback"));

    document.getElementById("choose").onclick = async function () {
      const query = document.getElementById("song-input").value;
      if (!query) return;
      const type = "track";
      const limit = 1;

      const results = await fetch(`https://api.spotify.com/v1/search?q=${query}&type=${type}&limit=${limit}`, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      const text = JSON.parse(await results.text());
      const track = text.tracks.items[0];

      await fetch("https://api.spotify.com/v1/me/player/play", {
        method: "PUT",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          uris: [track.uri],
        }),
      }).then(() => console.log(`chose song ${track.name}`));
    };

    document.getElementById("queue").onclick = async function () {
      console.log((await getQueue()).queue.map((x) => x.name));
    };
  });

  // Not Ready
  player.addListener("not_ready", ({ device_id }) => {
    console.log("Device ID has gone offline", device_id);
  });

  player.addListener("initialization_error", ({ message }) => {
    console.error(message);
  });

  player.addListener("authentication_error", ({ message }) => {
    console.error(message);
  });

  player.addListener("account_error", ({ message }) => {
    console.error(message);
  });

  document.getElementById("togglePlay").onclick = async function () {
    player.togglePlay();
  };

  player.connect();
};

fetch("http://localhost:5000/sendQuery", {
  method: "PUT",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify("dfgdfg"),
});
