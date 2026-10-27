import json, sys, subprocess, os
BASE = 'https://dmba1-byte.github.io/dmmotion/social/q/'
OUT = '/home/claude/reels/out2/'
def dur(n):
    return round(float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', OUT + n + '_silent.mp4'])), 2)
q = []
for j in json.load(open('/home/claude/reels/batch2.json')):
    n = j['name']
    q.append(dict(name=n, when_et=j['when'], hook=j['hook'].replace('<br>', ' '), caption=j['caption'], duration=dur(n),
                  video_url=BASE + n + '.mp4', silent_url=BASE + n + '_silent.mp4', music_url=BASE + n + '_music.mp3',
                  voice=j['voice'], ai_label=bool(j['voice']), status='pending_approval'))
for j in json.load(open('/home/claude/reels/extras.json')):
    n = j['name']
    q.append(dict(name=n, when_et=j['when'], hook=j['hook'], caption=j['caption'], duration=dur(j['src']),
                  video_url=BASE + n + '.mp4', silent_url=BASE + n + '_silent.mp4', music_url=BASE + n + '_music.mp3',
                  voice=j['voice'], ai_label=bool(j['voice']), status='pending_approval'))
q.sort(key=lambda e: e['when_et'])
json.dump(q, open(sys.argv[1], 'w'), indent=1, ensure_ascii=False)
print(len(q))
