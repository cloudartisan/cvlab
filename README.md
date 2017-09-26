```bash
brew install portaudio
pip install -r config/requirements.txt
```

If you encounter the following error:

```
OpenCV: error in [AVCaptureDeviceInput initWithDevice:error:]
2017-09-26 19:53:15.735 Python[81744:35863193] OpenCV: Cannot Use FaceTime HD Camera
OpenCV: camera failed to properly initialize!
```

Try the following:

```bash
sudo killall VDCAssistant
```
