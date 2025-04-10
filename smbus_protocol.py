import smbus2 as smb
from time import sleep

SMBUS_PROTOCOL_MANUFACTURING_ACCESS         =       0X00
SMBUS_PROTOCOL_REMAINING_CAPACITY_ALARM     =       0X01
SMBUS_PROTOCOL_REMAINING_TIME_ALARM         =       0X02
SMBUS_PROTOCOL_BATTERY_MODE                 =       0X03
SMBUS_PROTOCOL_AT_RATE                      =       0X04
SMBUS_PROTOCOL_AT_RATE_TIME_TO_FULL         =       0X05
SMBUS_PROTOCOL_AT_RATE_TIME_TO_EMPTY        =       0X06
SMBUS_PROTOCOL_AT_RATE_OK                   =       0X07
SMBUS_PROTOCOL_TEMPERATURE                  =       0X08
SMBUS_PROTOCOL_VOLTAGE                      =       0X09
SMBUS_PROTOCOL_CURRENT                      =       0X0A
SMBUS_PROTOCOL_AVERAGE_CURRENT              =       0X0B
SMBUS_PROTOCOL_MAX_ERROR                    =       0X0C
SMBUS_PROTOCOL_RELATIVE_STATE_OF_CHARGE     =       0X0D
SMBUS_PROTOCOL_ABSOLUTE_STATE_OF_CHARGE     =       0X0E
SMBUS_PROTOCOL_REMAIN_CAPACITY              =       0X0F
SMBUS_PROTOCOL_FULL_CHARGE_CAPACITY         =       0X10
SMBUS_PROTOCOL_RUN_TIME_TO_EMPTY            =       0X11
SMBUS_PROTOCOL_AVERAGE_TIME_TO_EMPTY        =       0X12
SMBUS_PROTOCOL_AVERAGE_TIME_TO_FULL         =       0X13
SMBUS_PROTOCOL_CHARGING_CURRENT             =       0X14
SMBUS_PROTOCOL_CHARGING_VOLTAGE             =       0X15
SMBUS_PROTOCOL_BATTERY_STATUS               =       0X16
SMBUS_PROTOCOL_CYCLE_COUNT                  =       0X17
SMBUS_PROTOCOL_DESIGN_CAPACITY              =       0X18
SMBUS_PROTOCOL_DESIGN_VOLTAGE               =       0X19
SMBUS_PROTOCOL_SPEC_INFO                    =       0X1A
SMBUS_PROTOCOL_MANUFACURING_DATE            =       0X1B
SMBUS_PROTOCOL_SERIAL_NUMBER                =       0X1C
SMBUS_PROTOCOL_MANUFACTURER_NAME            =       0X20
SMBUS_PROTOCOL_DEVICE_NAME                  =       0X21
SMBUS_PROTOCOL_DEVICE_CHEM                  =       0X22
SMBUS_PROTOCOL_MANUFACTURER_DATA            =       0X23

SMBUS_PROTOCOL_ERROR_CODE = ["OK", "BUSY", "RESERVED COMMAND", "UNSUPPORTED COMMAND", "ACCESS DENIED", "OVERFLOW/UNDERFLOW", "BADSIZE", "UNKNOWNERROR"]

SMBUS_BATTERY_PACK_LIFE_CYCLE_RRC2040       =       300
SMBUS_BATTERY_PACK_LIFE_CYCLE_RRC3570       =       300
SMBUS_BATTERY_PACK_LIFE_CYCLE_OTHER         =       400

class smb_protocol:
    OCA = 0
    TCA = 0
    OTA = 0
    TDA = 0
    RCA = 0
    RTA = 0
    INIT = 0
    DSG = 0
    FC = 0
    FD = 0
    EC3 = 0
    EC2 = 0
    EC1 = 0
    EC0 = 0
    
    def __init__(self, bus, addr = 0x0b):
        self.bus    = bus
        self.addr   = addr
        self.smb    = smb.SMBus(self.bus)
    
    def get_info(self):
        '''
        Display info of battery pack
        unit : -
        '''
        print("Device Part Number : " + self.get_device_id())
        print("Battery Chemistry : " + self.get_device_chem())
        print("Battery Pack Design Voltage: "+ str(self.get_fully_voltage()) + " V.")
        print("Battery Pack Design Capacity: "+ str(self.get_fully_capacity()) + " mAh.")
        print("Battery life : " + str(self.get_battery_life()) + " %.")
        
    def get_device_id(self):
        '''
        Get battery pack part number
        unit : -
        '''
        val = self.smb.read_i2c_block_data(self.addr, SMBUS_PROTOCOL_DEVICE_NAME, 8)
        res = ""
        for i in val:
            res = res + chr(i)
        return res
    
    def get_device_chem(self):
        '''
        Get battery cell chemistry
        unit : -
        '''
        val = self.smb.read_i2c_block_data(self.addr, SMBUS_PROTOCOL_DEVICE_CHEM, 5)
        res = ""
        for i in val:
            res = res + chr(i)
        return res
    
    def get_device_serial(self):
        '''
        Get device serial number
        unit : -
        '''
        val = self.smb.read_word_data(self.addr, SMBUS_PROTOCOL_DESIGN_VOLTAGE)
        return round(val / 1000, 3)
    
    def get_fully_voltage(self):
        '''
        Get design voltage of battery pack
        unit : V
        '''
        val = self.smb.read_word_data(self.addr, SMBUS_PROTOCOL_VOLTAGE)
        return round(val / 1000, 3)
    
    def get_fully_capacity(self):
        '''
        Get design capacity of battery pack
        unit : mAh
        '''
        val = self.smb.read_word_data(self.addr, SMBUS_PROTOCOL_DESIGN_CAPACITY)
        return val
    
    def get_voltage(self):
        '''
        Get the voltage of battery pack
        unit : V
        '''
        val = self.smb.read_word_data(self.addr, SMBUS_PROTOCOL_VOLTAGE)
        return round(val / 1000, 3)
    
    def get_current(self):
        '''
        Get the current of battery pack
        unit : A
        '''
        val = self.smb.read_word_data(self.addr, SMBUS_PROTOCOL_CURRENT)
        if val > 32767:
            val = -(65535 - val) / 1000.0
            return round(val,3)
        elif val <= 32767:
            val = val / 1000.0
            return round(val,3)
    
    def get_battery_temp(self):
        '''
        Get the temperature of battery pack
        unit : Celsius
        '''
        val = self.smb.read_word_data(self.addr, SMBUS_PROTOCOL_TEMPERATURE)
        return round((val * 0.1) - 273.15,3)
    
    def get_battery_percentage(self):
        '''
        Get battery level in percentage
        unit : %
        '''
        val = self.smb.read_word_data(self.addr, SMBUS_PROTOCOL_RELATIVE_STATE_OF_CHARGE)
        return val
    
    def get_battery_cycle(self):
        '''
        Get battery cycle
        unit : cycles
        '''
        val = self.smb.read_word_data(self.addr, SMBUS_PROTOCOL_CYCLE_COUNT)
        return val
    
    def get_battery_status(self):
        '''
        Get battery status
        unit : -
        OCA (Bit 15): Overcharged Alarm
        TCA (Bit 14): Terminate Charge Alarm
        OTA (Bit 12): Overtemperature Alarm
        TDA (Bit 11): Terminate Discharge Alarm
        RCA (Bit 9): Remaining Capacity Alarm
        RTA (Bit 8): Remaining Time Alarm
        INIT (Bit 7): Initialization
        DSG (Bit 6): Discharging or Relax
        FC (Bit 5): Fully Charged
        FD (Bit 4): Fully Discharged
        EC3,EC2,EC1,EC0 (Bits 3â€“0): Error Code
        '''
        val = self.smb.read_word_data(self.addr, SMBUS_PROTOCOL_BATTERY_STATUS)
        self.OCA     =   (val & 0x8000) >> 15
        self.TCA     =   (val & 0x4000) >> 14
        self.OTA     =   (val & 0x1000) >> 12
        self.TDA     =   (val & 0x0800) >> 11
        self.RCA     =   (val & 0x0200) >> 9
        self.RTA     =   (val & 0x0100) >> 8
        self.INIT    =   (val & 0x0080) >> 7
        self.DSG     =   (val & 0x0040) >> 6
        self.FC      =   (val & 0x0020) >> 5
        self.FD      =   (val & 0x0010) >> 4
        self.EC3     =   (val & 0x0008) >> 3
        self.EC2     =   (val & 0x0004) >> 2
        self.EC1     =   (val & 0x0002) >> 1
        self.EC0     =   (val & 0x0001) >> 0
        
        if self.OCA == 1:
            print("Overcharged has been detected")
        if self.TCA == 1:
            print("Charging has been terminated")
        if self.OTA == 1:
            print("Discharge has been terminated")
        if self.RCA == 1:
            print("Remaining Capacity is lower than 10% of full capacity")
        if self.INIT == 1:
            print("Gauge initialization is complete.")
        if self.DSG == 1:
            print("Battery is in discharge or relax mode.")
        else:
            print("Battery is in charge mode.")
        
        res = (self.EC2 << 2) + (self.EC1 << 1) + (self.EC0 << 0)
        print("The system is " + SMBUS_PROTOCOL_ERROR_CODE[res])
    
    def get_battery_life(self):
        '''
        Get battery life
        unit : %
        '''
        val = self.get_device_id()
        if val == "RRC2040":
            return round(((SMBUS_BATTERY_PACK_LIFE_CYCLE_RRC2040 - self.get_battery_cycle()) / SMBUS_BATTERY_PACK_LIFE_CYCLE_RRC2040) * 100)
        elif val == "RRC3570":
            return round(((SMBUS_BATTERY_PACK_LIFE_CYCLE_RRC3570 - self.get_battery_cycle()) / SMBUS_BATTERY_PACK_LIFE_CYCLE_RRC3570) * 100)
        else:
            return round(((SMBUS_BATTERY_PACK_LIFE_CYCLE_OTHER- self.get_battery_cycle()) / SMBUS_BATTERY_PACK_LIFE_CYCLE_OTHER) * 100)