import ipaddress

class cidr:
    def convert(cidr:str):
        list = []
        net = ipaddress.ip_network(cidr)
        for add in net:
            list.append(str(add))
        return list
