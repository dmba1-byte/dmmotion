# Voiceover — free, local, unlimited

Every DM Motion reel is voiced. This is not optional: a silent reel of a floor
plan loses people before they work out what they are looking at.

No API and no credits are involved. The voice is Piper, a neural TTS model that
runs on the CPU inside the build container.

## Restoring it in a fresh container

HuggingFace is blocked by the sandbox proxy. GitHub release assets are not, and
that is where this model comes from:

    pip install --break-system-packages piper-tts
    mkdir -p /home/claude/reels/voices && cd /home/claude/reels/voices
    curl -sL -o ryan.tgz \
      https://github.com/rhasspy/piper/releases/download/v0.0.2/voice-en-us-ryan-high.tar.gz
    tar xzf ryan.tgz && rm ryan.tgz

That leaves `en-us-ryan-high.onnx` (+ `.json`) in place, which is what `vo.py`
expects. The model is ~120 MB, over GitHub's file limit, so it is deliberately
NOT committed — re-download it.

Other voices on the same release tag: `en-us-libritts-high`, `en-us-ryan-medium`,
`en-us-amy-low`, `en-us-kathleen-low`. `en-us-lessac-high` and `en-us-amy-medium`
are NOT on that tag (404).

## Using it

    import vo
    vo.duration("Find what's wrong.")      # seconds, for timing the beats
    vo.mix_into(wav_path, [(t, line), ...]) # lays lines over a finished soundtrack

`mix_into` ducks the music under each line and normalises the result. Lines are
cached by content hash under `voices/cache/`, so a re-render costs nothing.

## Writing the script

Beats are cut to the voiceover, not the other way round — write the script
first, measure it with `vo.duration`, then set the beat times in `rules.py`.
Keep speech close to continuous; gaps are where viewers leave.
