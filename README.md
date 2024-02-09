# Spotify Poster Generator

https://spotifyposters.live/

Does what it says on the tin.

Enter a (valid) Spotify album URL, receive a poster!

## Examples!

<p style="text-align: center;">
  <img src="images/Honestly,_Nevermind_dark_poster.png" style="width: 49%;" alt="Poster 1"/>
  <img src="images/結束バンド_light_poster.png" style="width: 49%;" alt="Poster 2"/> 
</p>

---

## Usage

1. Build the `Dockerfile`:
    ```bash
    docker build . --name poster-generator
    ```
2. Run Gunicorn locally:
    ```bash
    docker run -d -p 3000:3000 docker.io/library/poster-generator
    ```

### Issues/Ideas
- [ ] Tracks vertical length scaling
- [ ] Drop down menu in main webpage to search for album
  
### Fixed Issues 🎉
- [x] Choose poster size
- [x] Special characters not supported
- [x] Better font
- [x] No checking for validity of URL
---
To run this for yourself locally, you'll need a .env file with the following values:
- SPOTIFY_SECRET = `your spotify secret code`
- SPOTIFY_ID = `your spotify client id`
- FLASK_SECRET = `your flask secret code`

---
Big thanks to [@sudmike](https://github.com/sudmike) for contributing to the repository and coming up with ideas!
> The website probably won't be up all the time, just email me if you need one.
