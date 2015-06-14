#!/bin/bash
set -e
playlistdir=/var/lib/mpd/music/WEBRADIO
printf "Generating BBC playlists.."

declare -A radios
#radios["Default"]="http://www.radiofeeds.co.uk/bbcradio4fm.pls"
radios["BBC Radio 1"]="http://www.radiofeeds.co.uk/bbcradio1.pls"
radios["BBC Radio 2"]="http://www.radiofeeds.co.uk/bbcradio2.pls"
radios["BBC Radio 3"]="http://www.radiofeeds.co.uk/bbcradio3.pls"
radios["BBC Radio 4"]="http://www.radiofeeds.co.uk/bbcradio4fm.pls"
radios["BBC Radio 5 Live"]="http://www.radiofeeds.co.uk/bbc5live.pls"
radios["BBC Radio 5 Live SX"]="http://www.radiofeeds.co.uk/bbc5livesportsextra.pls"
radios["BBC 6 Music"]="http://www.radiofeeds.co.uk/bbc6music.pls"


for k in "${!radios[@]}"
do
filepath="${playlistdir}/${k}.m3u"
rm -f "$filepath"
echo "#EXTM3U" >> "$filepath"
pls=${radios[$k]}
echo "#EXTINF:-1, BBC - $k" >> "$filepath"
curl -s $pls | grep File1 | sed 's/File1=\(.*\)/\1/' >> "$filepath"
done
printf ".... generated\n"
