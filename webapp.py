"""
     This file is part of poster-gen.

    poster-gen is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

    poster-gen is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with poster-gen. If not, see <https://www.gnu.org/licenses/>.
"""

from flask import Flask, render_template, request, send_file, redirect
from poster_generator import generator
import io
from dotenv import load_dotenv
import os
import re
import requests

load_dotenv()

app = Flask(__name__, instance_relative_config=True)
app.config["SECRET_KEY"] = os.getenv('FLASK_SECRET')


@app.route('/')
def index():
    return render_template('mainpage.html')


@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method != 'POST':
        # redirect to home screen if result page is called in browser
        return redirect('/')
    album_link = request.form["album_input"]
    width = 3300 if 'width' not in request.form or not request.form["width"].isnumeric() else int(request.form["width"])
    height = 5100 if 'height' not in request.form or not request.form["height"].isnumeric() else int(
        request.form["height"])

    # check that input is not empty
    if album_link == "" or album_link is None:
        return render_template('mainpage.html', warning_notification='Input field cannot be empty')

    # check values for height and width
    if width < 300 or height < 450:  # width and height have minimum requirements
        return render_template('mainpage.html',
                               warning_notification='Width must be at least 300px and height must be at least 450px')
    if height < width * 1.25 or height > width * 2:  # height must be between 30% and 100% larger than width
        return render_template('mainpage.html',
                               warning_notification='Height must be between 25% and 100% larger than width')

    # get color theme of poster
    theme = request.form["theme"]
    # check if featured artists are to be removed from track
    remove_featured = request.form.get("remove_featured_artists")
    options = {
        'theme': theme,
        'remove_featured_artists': remove_featured == 'true',
    }
    if re.match(r'https://spotify.link/([a-zA-Z0-9]+)', album_link):
        album_link = requests.get(album_link).url

    patterns = [
        r'^https://open\.spotify\.com/album/([a-zA-Z0-9]+)',
        r'^spotify:album:([a-zA-Z0-9]+)',
    ]

    if not any(re.match(pattern, album_link) for pattern in patterns):
        return render_template('mainpage.html', warning_notification='Invalid album link')

    # generate poster
    poster, album_name = generator(album_link, (width, height), options)

    # check that album data was fetched
    if poster is None or album_name is None:
        return render_template('mainpage.html',
                               warning_notification=f'Failed to get album data based on input "{album_link}"')

    poster_bytes = io.BytesIO()
    poster.save(poster_bytes, "png")
    poster_bytes.seek(0)

    return send_file(
        poster_bytes,
        mimetype='image/png',
        download_name=f"{album_name}_{theme}_poster.jpg",
        as_attachment=True
    )


if __name__ == '__main__':
    app.run(debug=True)
