# Balloon telemetry decoder 


### Compilation

    gcc BalloonPos.cpp -o BalloonPos

### Usage 

    ./BalloonPos

Then enter the sigfox message. For example: 23a0fc0a3c1300f606c20993
You should get following as output: 

![Decoded Balloon position from sigfox message](example_screenshot.png "Sigfox decoder output")

