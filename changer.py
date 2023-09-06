#!/usr/bin/python3

import platform
import enum
import os

GMD_ORIGINAL_SERVER = 'www.boomlings.com'  # do not change this

class PlatformType(enum.Enum):
    Windows = 1
    Linux = 2
    Mac = 3

    @staticmethod
    def get_current_platform():
        current_platform = platform.system()
        if current_platform == "Windows":
            return PlatformType.Windows
        elif current_platform == "Linux":
            return PlatformType.Linux
        elif current_platform == "Darwin":
            return PlatformType.Mac
        else:
            raise Exception("Unsupported platform: " + current_platform)
        
    def get_host_file_path():
        current_platform = PlatformType.get_current_platform()
        if current_platform == PlatformType.Windows:
            return r"C:\Windows\System32\drivers\\etc\\hosts"
        elif current_platform == PlatformType.Linux:
            return "/etc/hosts"
        elif current_platform == PlatformType.Mac:
            return "/private/etc/hosts"
        else:
            raise Exception("Unsupported platform: " + current_platform)


class Program:
    def print_header(self):
        os.system("cls" if os.name == "nt" else "clear")
        print("GMD Server Changer v0.1")
        print("")
        print("This program will change the GMD server to the one you want.")
        print("")
        print("Current OS: " + str(PlatformType.get_current_platform()))
        print("Host file path: " + PlatformType.get_host_file_path())
        print("")

    def read_hosts_file(self, backup=False):
        host = PlatformType.get_host_file_path()
        if backup:
            host += ".bak"
        with open(host, "r") as f:
            return f.readlines()
        
    def change_ip(self):
        hosts = self.read_hosts_file()
        if not GMD_ORIGINAL_SERVER in hosts:
            print("[!] not backup hosts file found")
            print("[!] make a backup hosts file")
            with open(PlatformType.get_host_file_path() + ".bak", "w") as f:
                f.writelines(hosts)
        else:
            print("[!] backup hosts file found")
            print("[!] use backup hosts file")
            with open(PlatformType.get_host_file_path(), "w") as f:
                f.writelines(
                    self.read_hosts_file(backup=True)
                )

        new_ip = input("[+] Enter the new GMD server ip: ")
        with open(PlatformType.get_host_file_path(), "a") as f:
            f.write("\n" + new_ip + " " + GMD_ORIGINAL_SERVER)

        print("[+] Done! Now you can play GMD with your own server!")
        print("[+] If you want to restore the original server, just delete the last line in the hosts file.")
        print("[+] Enjoy!")

    def backup_hosts_file(self):
        hosts = self.read_hosts_file()

        if os.path.exists(PlatformType.get_host_file_path() + ".bak"):
            print("[!] backup hosts file found")
            print("[!] use backup hosts file")
            with open(PlatformType.get_host_file_path(), "w") as f:
                f.writelines(
                    self.read_hosts_file(backup=True)
                )
        else:
            print("[!] not backup hosts file found")
            print("[!] make a backup hosts file")
            with open(PlatformType.get_host_file_path() + ".bak", "w") as f:
                f.writelines(hosts)

    def start(self):
        self.print_header()
        print("")
        print("1. Change GMD server")
        print("2. Backup hosts file")
        print("3. Exit")
        print("")
        choice = input("[+] Enter your choice: ")

        if choice == "1":
            self.change_ip()
        elif choice == "2":
            self.backup_hosts_file()
        elif choice == "3":
            exit(0)
        else:
            print("[!] Invalid choice")
            self.start()


if __name__ == "__main__":
    Program().start()
