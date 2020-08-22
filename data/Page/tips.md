---
path: /speakers/tips
---
# How to look (and sound) good in your talk

<iframe width="640" height="360" src="https://www.youtube.com/embed/C1TBqdULp4E" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

We've prepared a Tech Tips video: How to get the best from your remote presentation; click above to watch.

[This PDF by Kubecon EU is also very useful](https://events.linuxfoundation.org/wp-content/uploads/2020/06/KubeCon_EU_Virtual_2020_WebPresenterDoc_v4.pdf), recommend reading.

If you decide to buy additional hardware (note COVID is making stock levels challenging, order early), please make sure you put the time in to properly test before the event.  It’s unfortunately common to see someone buy an awesome new microphone to have them accidentally not have it set as the active recording audio device during their talk, or not have it placed in front of them correctly.

## Microphone / audio quality

By far, the best investment is ensuring audio quality is clear and not echo-y.  **This is more important than video quality.** Using your laptop microphone is OK for short talks or video chat, but the echo will get very fatiguing to listen to for a 20+ minute talk.

In an ideal world; a external USB condenser microphone is your best bet, but you will need to practice with it to ensure you’re getting optimal audio levels, it’s positioned correctly, it doesn’t accidentally pickup your speakers/other sound during your talk, and make sure any gain or volume controls are set so it's loud and clear, without any distortion, even when you're speaking loudly into it.

Many podcasting guides are very useful to read, for example: https://www.buzzsprout.com/blog/mic-technique-podcasting

Dropping down from this, using a USB headset with a microphone is the next best thing.

Practice by recording some audio in something like Audacity, and listen to the difference in audio quality between your laptop microphone or the positioning of the microphone.  Pay attention to the audio control panel in your OS to ensure you are positioned in front of the microphone correctly (if you are using an analog microphone).

When presenting, try to isolate yourself away from any background/ambient noise (close windows and doors, away from people if possible, etc).

## Cameras & lighting

Some laptop webcams work pretty well (i.e. those in a MacBook); others aren’t so good.  An external USB webcam such as a Logitech C920 is a relatively affordable way to add high quality video.

That said, before you do that, make sure you’re in a well lit position - it’s surprising how much difference this makes to quality.  Lighting should be in front of you (facing back towards you), with no visible lights behind you.

An easy/cheap way to ensure you’re well lit is to sit facing a window: but keep in mind the time of day when you test, compared to the time of day when you are presenting.

## Camera positioning

Make sure you are filling the frame - you don’t want your head at the bottom of the shot with lots of empty space!

If you can (especially if you have an external webcam and microphone), present standing up rather than sitting down.  May sound silly, but it will help considerably with your presence.  If you do this, ensure your webcam is level or facing down at you, though, rather than pointing up (a stand may help).

If you’re feeling particularly creative, you could even consider a more professional setup with a dedicated HDMI camera and tripod, wireless lapel microphone, lighting and backdrop, but a decent external webcam and external microphone can get you most of the way there.

## Internet connection

If you can, a wired Internet connection is going to beat the pants of a wireless connection.  Latency/jitter/dropouts (which are more likely to occur on wifi) especially affect video streaming.

Streaming at 720p ideally requires over 2mbit, with a minimum of 1mbit for OK quality. 5mbit or higher is highly recommended (i.e.a NBN 25/5 connection or higher).   When you are presenting, strong recommendation to ensure nobody else in your household is utilising upload bandwidth (i.e. peer to peer applications).

## Timer, power & second monitor/device

Having a timer displayed (on a second monitor, device, phone) with a countdown will help you keep on time.

If you’re streaming, and you’re using speaker notes, keep in mind you’ll also need to keep the relevant chat channel / stream feed back to you open, so you can be communicated with during your talk if required.  It is possible you may need a third monitor or another device if your speaker notes take over the other screen, but testing/practice will reveal this.

Ensure all devices you are using are powered, and any settings such as automatic screen sleep or screen savers are turned off.

## Slide tips

Here are some suggestions for slide design that will help you avoid a few common disappointing situations that presenters can face. (We thank previous PyCon AU organisers for this helpful list).

- Ensure that text isn’t too close to the borders or sides of your slides
    - Projectors have a tendency to cut the sides of your slides!
        - Avoid highly indented bullet points
            - It’s a sign you’re overloading the slide.
            - With too much information.
                - Which can get frustrating
- Ensure that text is large enough to be readable at a distance (> 18 point is usually a good guide). If you can read your slide in the thumbnail preview, that is a good sign.
- Projectors - compared to screens - often have very poor contrast. Just because it looks good on your computer screen doesn't mean it will look good on the projector. Avoid too many fancy colours - just keep it simple.
- Many people have problems with seeing low contrast colours and images. Please also try to consider colour-blind people when picking colours.
- Spellcheck your presentation.
- Consider using a slide lint tool, such as http://slidelint.net/, to check your slides for many of the above conditions.

- More helpful hints can be found in the Writing Slides section of [VM Brasseur’s Public Speaking Resources](https://github.com/vmbrasseur/Public_Speaking#writing-presentations).

## Tips for pre-recording

You have two options:

- Screencaster (easiest, but either no webcam, or limited embed)
- Video editing (capture separate webcam/display, edit in a video editor)

Focus primarily on clear audio, and clear slides or screen capture.  Clear audio hands down is the most important aspect of an engaging video.  See our tech tips below for some advice.

We strongly encourage you to embed your webcam too; you may prefer not being in the shot, but having a talking speaker in the shot does make the video more engaging; and being able to see a presenter speak can increase video accessibility (i.e. auditory processing difficulties).

Please be aware that editing your video needs to be done by you&mdash;and that requesting changes after the due date is not possible.  The AV team is expecting to have many hours of video to work through so we likely will not have the capacity to do special pre-event edits ourselves.

For an embedded permanent Picture-in-Picture (i.e. screen sharing or basic video editing), recommend a simple view where you are keeping the webcam statically in the bottom right like below;

![](/assets/ryan-yaml.png)

For video editing, you can swap between a shot like this, a full screen webcam capture, and a full screen screen share (or whatever shots you want!).

## Software Suggestions

- [PanOpto's free web-based recorder (cross-platform)](https://www.panopto.com/record/)
    - Easy to use, allows webcam embed (go to settings, enable Capture in HD and Smart Camera), and will give you a WebM locally at the end.
- [OBS (multi-platform)](https://obsproject.com/)
    - Open source streaming software, but will let you record a video locally (don’t have to stream) and you can embed a Picture-in-Picture webcam view inside of a screen share.  Little more of a learning curve than other software but lots of guides online and relatively intuitive to use.
    - If you’re feeling creative, you can hook this up to an external set of buttons, and change views during your talk (swap between fullscreen camera, screen share, or Picture-in-Picture like above).
- [aPowersoft’s free screen recorder (Windows, OS X)](https://www.apowersoft.com/free-online-screen-recorder?__c=1)
    - Requires local installation, but easy to use, allows webcam embed (recommend making it larger) and works relatively well, with no time limitations or watermarks.  Will save locally as MP4.
- [Camtasia (Windows, OS X)](https://www.techsmith.com/video-editor.html)
    - The bells and whistles screen capture software which includes easy to use editing tools, but almost AUD$400 a licence.
- [Screencastify (Chrome plugin, cross-platform)](https://www.screencastify.com/)
    - Easy to use, allows webcam embed, uploads to Google Drive or MP4 download.
    - Free version only gives 5 minutes, licenced version is $49/year.
- [SimpleScreenRecorder](https://github.com/MaartenBaert/ssr), or [Kazam](https://launchpad.net/kazam) (Linux),
    - Easy to use, open source, free, but no webcam embed

## Other Suggestions

- Using an external camera with microphone, screen-sharing, editing later
    - Recording with an external camera to SD, while simultaneously recording a screen share, and then editing it in a non-linear editor such as Adobe Premiere will net you pretty good results and give you maximum flexibility over editing options, but take a bit of time.
- Pre-recording your talk during the practice/test days
    - For a small percentage of talks, we can pre-record your entire talk using the streaming infrastructure on the practice/test days: we would like to do this for a handful of talks in any case.  Please let us know.
- Dedicated capture hardware and post-production
    - For the ultimate in quality, using a dedicated camera (recording directly to SD card or HDMI/SDI capture) and capturing a screen capture as separate files and post-producing them in an editor such as Adobe Premiere will give you the most flexibility.  Something like an ATEM Mini could be considered for multi-camera productions, but this is a significantly more expensive solution that requires high time investment.

You are welcome (and encouraged) to provide a small sample recording for the AV team to review in advance.  This can be uploaded to the same place as the other videos (details to be provided if you opt in to pre-recording).
