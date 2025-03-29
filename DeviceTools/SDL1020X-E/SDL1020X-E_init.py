import pyvisa

rm = pyvisa.ResourceManager()
inst = rm.open_resource('TCPIP0::192.168.178.148::inst0::INSTR')
print(inst.query(':SENSe:FREQuency:CENTer? '))
