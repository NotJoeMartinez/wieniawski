# Wieniawski

Experimental refactor of [Mozart](https://github.com/aashrafh/Mozart) optical music recognition models.
See music [MusicNotesML](https://github.com/NotJoeMartinez/MusicNotesML) for a proof of concept. 


### Setup 
```
git clone https://github.com/NotJoeMartinez/wieniawski
cd wieniawski
python3 -m venv .venv
source .venv/bin/activate
make clean install
```

### Training data

- [google drive](https://drive.google.com/file/d/18YngVnanqM26qJwm8HrrDwqMK3KLSGPV/view?usp=sharing)
    - Orginal dataset
- [kaggle](https://www.kaggle.com/datasets/notjoemartinez/mozart)
    - slightly modifed for kaggle compatablity


### Goals 
1. To understand how this model works
2. To integrate the models with a mobile application that overlays the proper finger numbers of a stanza violin sheet music.  