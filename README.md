# Video to subtitle files

copy the env and put your api
```bash
cp .envcopy .env
```

2. put any zoom record in the vido folder (output/video), the system now taking auto the first file there so make sure there is only one file there.
3. run [main.py](main.py) and then u will get data in output/audio folder
4. delete the full mp3 that in audio folder.
5. run the [Spechtotext.py](Spechtotext.py)
6. in the output/text folder there is all the cunks text.

---

- [ ] Change the [main.py](main.py) for the code will not save in the end the full size of the mp3 sound.  