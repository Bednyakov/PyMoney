import pymem
import pymem.process
import ctypes

class MemoryEditor:
    def __init__(self, process_name: str) -> None:
        self.pm = pymem.Pymem(process_name)
        self.process_base = pymem.process.module_from_name(self.pm.process_handle, process_name).lpBaseOfDll
    
    def search_value(self, value: int) -> list:
        search_results = []
        memory_size = 0x7FFFFFFF  # Размер памяти для сканирования (большой диапазон)
        chunk_size = 0x1000  # Размер блока чтения
        search_bytes = ctypes.c_uint32(value).value.to_bytes(4, byteorder='little')
        
        offset = 0
        while offset < memory_size:
            current_address = self.process_base + offset
            
            if self.is_memory_readable(current_address):
                try:
                    buffer = self.pm.read_bytes(current_address, chunk_size)
                except pymem.exception.MemoryReadError:
                    offset += chunk_size
                    continue
                
                chunk_offset = 0
                while True:
                    chunk_offset = buffer.find(search_bytes, chunk_offset)
                    if chunk_offset == -1:
                        break

                    # Сохранение адреса найденного значения
                    address = current_address + chunk_offset
                    search_results.append(address)
                    
                    chunk_offset += len(search_bytes)
            
            offset += chunk_size

        return search_results
    
    def search_next_value(self, addresses: list, next_value: int) -> list:
        search_results = []
        search_bytes = ctypes.c_uint32(next_value).value.to_bytes(4, byteorder='little')
        
        for address in addresses:
            if self.is_memory_readable(address):
                try:
                    buffer = self.pm.read_bytes(address, 4)
                except pymem.exception.MemoryReadError:
                    continue
                
                if buffer == search_bytes:
                    search_results.append(address)
        
        return search_results
    
    def replace_value(self, addresses: list, new_value: int) -> None:
        replace_bytes = ctypes.c_uint32(new_value).value.to_bytes(4, byteorder='little')
        for address in addresses:
            self.pm.write_bytes(address, replace_bytes, 4)
            print(f"Замена значения по адресу: {hex(address)} на {new_value}")
    
    def is_memory_readable(self, address) -> bool:
        mbi = pymem.memory.virtual_query(self.pm.process_handle, address)
        if mbi.Protect & 0xF != 0x0 and mbi.State == 0x1000 and mbi.Protect & 0x100 == 0:
            return True
        return False