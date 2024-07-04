import logging

def logging_configuration(logger):
    sh_formatter = logging.Formatter(fmt='%(asctime)s %(process)d %(name)s %(levelname)s %(funcName)s %(message)s',
                                     datefmt='%d-%b-%y %H:%M:%S')
    sh = logging.StreamHandler()
    sh.setLevel(level=logging.INFO)
    sh.setFormatter(sh_formatter)

    logger.setLevel(logging.DEBUG)
    logger.addHandler(sh)

if platform.system() == "Windows":
    hactoolnet = "./tools/hactoolnet-windows.exe"
    hactool = "./tools/hactool-windows.exe"
elif platform.system() == "Linux":
    hactoolnet = "./tools/hactoolnet-linux"
    hactool = "./tools/hactool-linux"
elif platform.system() == "MacOS":
    hactoolnet = "./tools/hactoolnet-macos"
    hactool = "./tools/hactool-macos"
else:
    logger_interface.warning(f"Unknown Platform: {platform.system()}, proide your own hactoolnet")
    hactoolnet = "hactoolnet"
    hactool = "hactool"
