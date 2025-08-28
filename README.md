## Steps

1. create a folders name video and audio



2. put any zoom record in the vido folder, the system now taking auto the first file there so make sure there is only one file there.
3. run [main.py](main.py) and then u will get data in audio folder
4. delete the full mp3 that in audio folder.
5. copy the env and put your api
```bash
cp .envcopy .env
```
6. run the [Spechtotext.py](Spechtotext.py)




---
# for running the site

go to "Shai" folder and run:
```bash
docker build -t lesson-site .
```

the run

```bash
docker run -p 8000:8000 lessons-site
```

the site run on:
```
http://localhost:8000
```


---
ToDo

- [ ] Change the [main.py](main.py) for the code will not save in the end the full size of the mp3 sound.  