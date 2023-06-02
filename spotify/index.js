const express = require("express");
const dotenv = require("dotenv");
const request = require("request");
const path = require("path");

const port = 5000;
let access_token = "";
let query;

dotenv.config();

let spotify_client_id = process.env.SPOTIFY_CLIENT_ID;
let spotify_client_secret = process.env.SPOTIFY_CLIENT_SECRET;

let spotify_redirect_uri = `http://localhost:${port}/auth/callback`;

let generateRandomString = function (length) {
  let text = "";
  let possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

  for (let i = 0; i < length; i++) {
    text += possible.charAt(Math.floor(Math.random() * possible.length));
  }
  return text;
};

let app = express();

app.get("/", (req, res) => {
  if (!access_token) return res.redirect("/auth/login");
  app.use(express.static("public"));
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

app.get("/auth/login", (req, res) => {
  let scope =
    "streaming user-read-email user-read-private user-read-playback-state user-modify-playback-state user-read-currently-playing playlist-read-private playlist-read-collaborative user-read-playback-position";

  let state = generateRandomString(16);

  let auth_query_parameters = new URLSearchParams({
    response_type: "code",
    client_id: spotify_client_id,
    scope: scope,
    redirect_uri: spotify_redirect_uri,
    state: state,
  });

  res.redirect("https://accounts.spotify.com/authorize/?" + auth_query_parameters.toString());
});

app.get("/auth/callback", (req, res) => {
  let code = req.query.code;

  let authOptions = {
    url: "https://accounts.spotify.com/api/token",
    form: {
      code: code,
      redirect_uri: spotify_redirect_uri,
      grant_type: "authorization_code",
    },
    headers: {
      Authorization: "Basic " + Buffer.from(spotify_client_id + ":" + spotify_client_secret).toString("base64"),
      "Content-Type": "application/x-www-form-urlencoded",
    },
    json: true,
  };

  request.post(authOptions, function (error, response, body) {
    if (!error && response.statusCode === 200) {
      access_token = body.access_token;
      res.redirect("/");
    }
  });
});

app.get("/getToken", (req, res) => {
  res.send(access_token);
});

app.get("/favicon.ico", (req, res) => {
  res.sendStatus(204);
});

app.put("/sendQuery", (req, res) => {
  query = req.body;
  console.log(query);
});

app.listen(port, () => {
  console.log(`Listening at http://localhost:${port}`);
});
