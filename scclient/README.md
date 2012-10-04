# scclient - SemioCoder Client

scclient is a very simple lightweight client for

## Installing

Just copy the module in your Python project 

## Running

Make sure the module is in your PYTHONPATH

```bash
Python 2.7.3 (default, Apr 10 2012, 23:31:26) [MSC v.1500 32 bit (Intel)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> from scclient import client
>>> con = client.Semiocoder('http://127.0.0.1:8000', verbose=True)
>>> con.login('user', 'password')
>>> con.getEncoders()
<?xml version="1.0" ?><encoders>
        <encoder>
                <outputflag/>
                <inputflag>-i</inputflag>
                <id>1</id>
                <name>ffmpeg</name>
        </encoder>
</encoders>
<xml.dom.minidom.Document instance at 0x028CD7D8>
>>>
```
