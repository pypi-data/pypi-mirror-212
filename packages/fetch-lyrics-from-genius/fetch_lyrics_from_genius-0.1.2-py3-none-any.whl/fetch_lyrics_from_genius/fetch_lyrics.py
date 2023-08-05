import argparse
import os
import re
import lyricsgenius
import musicbrainzngs
from slugify import slugify

# Set up the musicbrainzngs library
musicbrainzngs.set_useragent("Karaoke Hunt", "0.1", "https://github.com/karaokenerds/lyrics-from-genius")

def clean_lyrics(lyrics):
    lyrics = lyrics.replace('\\n', '\n')
    lyrics = re.sub(r'You might also like', '', lyrics)
    lyrics = re.sub(r'.*?Lyrics([A-Z])', r'\1', lyrics)  # Remove the song name and word "Lyrics" if this has a non-newline char at the start
    lyrics = re.sub(r'[0-9]+Embed$', '', lyrics)  # Remove the word "Embed" at end of line with preceding numbers if found
    lyrics = re.sub(r'(\S)Embed$', r'\1', lyrics)  # Remove the word "Embed" if it has been tacked onto a word at the end of a line
    lyrics = re.sub(r'^Embed$', r'', lyrics)  # Remove the word "Embed" if it has been tacked onto a word at the end of a line
    lyrics = re.sub(r'.*?\[.*?\].*?', '', lyrics)  # Remove lines containing square brackets
    # add any additional cleaning rules here
    return lyrics

def write_lyrics_file(song_title, artist_name, lyrics, album_name=False, track_num=False):
    # Replace any non-filename safe characters with a hyphen in the song title and artist name
    artist_name = slugify(artist_name, lowercase=False)
    song_title = slugify(song_title, lowercase=False)

    if album_name is not False:
        album_name = slugify(album_name, lowercase=False)
        directory = f'lyrics/{artist_name}/{album_name}'
    else:
        directory = f'lyrics/{artist_name}'
        
    if not os.path.exists(directory):
        os.makedirs(directory)

    if track_num is not False:
        song_title = f'{track_num}.{song_title}'

    filename = f'{directory}/{song_title}.txt'
    with open(filename, 'w') as f:
        f.write(lyrics)


def main():
    parser = argparse.ArgumentParser(description='Fetch lyrics from Genius.com and write them to text files')
    parser.add_argument('artist_name', type=str, help='the name of the artist to fetch lyrics for')
    parser.add_argument('--album_title', type=str, help='(optional) the title of a specific album to fetch all lyrics for')
    parser.add_argument('--song_title', type=str, help='(optional) the title of a specific song to fetch lyrics for')
    parser.add_argument('--max_songs', type=int, default=3, help='(optional) the maximum number of songs to fetch lyrics for (default=100)')
    parser.add_argument('--api_token', type=str, help='(optional) the API token for Genius.com')
    args = parser.parse_args()

    if args.api_token:
        genius = lyricsgenius.Genius(args.api_token)
    elif 'GENIUS_API_TOKEN' in os.environ:
        genius = lyricsgenius.Genius(os.environ['GENIUS_API_TOKEN'])
    else:
        print('Please provide an API token either as a command line argument or as the GENIUS_API_TOKEN environment variable')
        return

    if args.song_title:
        # fetch lyrics for a specific song
        song = genius.search_song(args.song_title, args.artist_name)
        if song is None:
            print(f'Could not find lyrics for "{args.song_title}" by {args.artist_name}')
            return
        lyrics = clean_lyrics(song.lyrics)
        write_lyrics_file(song.title, song.artist, lyrics)
        print(f'Successfully fetched lyrics for "{song.title}" by {song.artist}')
    elif args.album_title:
        
        # Search for the album by the artist
        album_result = musicbrainzngs.search_releases(query=args.album_title, artist=args.artist_name, limit=1, primarytype = 'Album')

        # If there are no search results, exit with an error message
        if len(album_result['release-list']) == 0:
            print(f"No albums found for the given artist and album name")
        else:
            album = album_result['release-list'][0]
            album_year = album["date"][:4]
            print(f"Album found: '{album['title']}' ({album_year}) with ID: {album['id']}")

            album_data = musicbrainzngs.get_release_by_id(album['id'], includes=['recordings']);
            album_tracks = (album_data["release"]["medium-list"][0]["track-list"])
            for x in range(len(album_tracks)):
                track = (album_tracks[x])
                title = track["recording"]["title"]
                print(f'Fetching lyrics for track {track["number"]}. {title}')

                song = genius.search_song(title, args.artist_name)
                if song is None:
                    print(f'Could not find lyrics for "{title}" by {args.artist_name}')
                    return
                lyrics = clean_lyrics(song.lyrics)
                write_lyrics_file(song.title, song.artist, lyrics, album_name=album['title'], track_num=track['number'])
                print(f'Successfully fetched lyrics for "{song.title}" by {song.artist}')

    else:
        # fetch lyrics for all songs by the artist
        artist = genius.search_artist(args.artist_name, max_songs=args.max_songs)
        if artist is None:
            print(f'Could not find lyrics for {args.artist_name}')
            return
        for i, song in enumerate(artist.songs):
            try:
                lyrics = clean_lyrics(song.lyrics)
                write_lyrics_file(song.title, song.artist, lyrics)
                print(f'Successfully fetched lyrics for "{song.title}" by {song.artist}')
            except Exception as e:
                print(f'Error processing song {i}: {e}')
                continue

if __name__ == '__main__':
    main()
