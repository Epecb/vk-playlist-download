# VK user playlist download

Tool for get link to download mp3 files from playlist in the russian social network vk.com. Output - bash script.

## Prerequisites:
- Python 3.x
- bash
- ffmpeg

## Usage:
    {prog_name} [option]

    Options:
        update            - update playlist (save in playlist_file)
        info              - show song count (in playlist_file)
        info name         - list all song name and position number
        position [number] - get 10 link to songs
        save              - create template config.json
        help, --help, -h  - view this text

## First start
    {prog_name} save
    and edit config.json

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
