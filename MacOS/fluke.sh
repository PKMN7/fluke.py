#!/bin/bash

sudo tcpdump -nn -v -i en0 -s 1500 -c 1 'ether[20:2] == 0x2000' > fullflukeinfo.txt
Port="$(cat fullflukeinfo.txt | grep Port-ID)"
Address="$(cat fullflukeinfo.txt | grep -m 1 Address)"
Name="$(cat fullflukeinfo.txt | grep Device-ID)"

Name="$(echo "${Name}" | cut -d\' -f2)"
Address="$(echo "${Address}" | cut -d\  -f9)"
Port="$(echo "${Port}" | cut -d\' -f2)"
echo "${Name},${Address},${Port}"
