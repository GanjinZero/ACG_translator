import os

def generate_str_for_downloader(per_count=10000):
    song_set = set()
    for root, dirs, files in os.walk("./text/Lyrics"):
        for name in files:
            if name[-4:] == ".txt":
                with open(os.path.join(root, name), "r", encoding="utf-8") as f:
                    lines = f.readlines()
                for line in lines:
                    try:
                        song_set.update([int(line.strip())])
                    except BaseException:
                        pass
    
    song_list = list(song_set)
    #print(song_list[0:10])
    with open("./text/Lyrics/song_id_all", "w", encoding="utf-8") as f:
        for i in range(len(song_list) // per_count + 1):
            use_song = song_list[i * per_count: min(len(song_list), (i + 1) * per_count)]
            f.write(",".join([str(song) for song in use_song]) + "\n")

def main():
    generate_str_for_downloader()

if __name__ == "__main__":
    main()
