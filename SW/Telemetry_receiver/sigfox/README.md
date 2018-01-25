# CLI based Balloon telemetry decoder 


### Compilation

    gcc BalloonPos.cpp -o BalloonPos

### Usage 

    ./BalloonPos

Then enter the sigfox message. For example: 23a0fc0a3c1300f606c20993
You should get following as output: 

![Decoded Balloon position from sigfox message](example_screenshot.png "Sigfox decoder output")

# Web based Balloon telemetry decoder 

### Usage 

    python habitat_sigfox_uploader.py LetFik3

### Testing
 
    curl -G --data "data=23a0fc0a3c1300f606c20993" localhost:8080

![Decoded Balloon position from sigfox API](sigfox_web_interface.png "Sigfox Web interface decoder")


