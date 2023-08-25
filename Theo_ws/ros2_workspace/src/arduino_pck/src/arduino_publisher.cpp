import serial
ser = serial.Serial(
    port='COM1',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)
print(ser.portstr) #연결된 포트 확인.
ser.write(bytes('hello', encoding='ascii')) #출력방식1
ser.write(b'hello') #출력방식2
ser.write(b'\xff\xfe\xaa') #출력방식3
#출력방식4
vals = [12, 0, 0, 0, 0, 0, 0, 0, 7, 0, 36, 100] 
ser.write(bytearray(vals))
ser.read(ser.inWaiting()) #입력방식1
ser.close()

